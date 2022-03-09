import os.path

from matflow.exceptionpackage import MatFlowException
from matflow.database.DatabaseTable import DatabaseTable
from matflow.workflow.workflow_instance import WorkflowInstance
from matflow.workflow.database_version import DatabaseVersion
from matflow.workflow.version_number import VersionNumber
from pathlib import Path
from typing import Dict, List


class WorkflowData:
    __instance = None
    __databaseTable: DatabaseTable = DatabaseTable.get_instance()

    @staticmethod
    def get_instance():
        if WorkflowData.__instance is None:
            WorkflowData()
        return WorkflowData.__instance

    def __init__(self):
        if WorkflowData.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            WorkflowData.__instance = self

    def __get_key_of_workflow_version(self, wf_name: str, version: str) -> str:
        """Returns: index of workflow version"""
        get_version_key_query = (
            "SELECT ID FROM Version WHERE wfName = %s AND version = %s;"
        )
        version_key = self.__databaseTable.get_one(
            get_version_key_query, (wf_name, version)
        )
        return version_key[0]

    def create_wf_instance(self, wf_in: WorkflowInstance, conf_dir: Path):
        """Create a new instance of a workflow by using the dag-File of a Template with the Version set to 1.

        Check for duplicate workflow, only then create new entry. Throw error if workflow name is already taken.

        Args:
            wf_in(WorkflowInstance): new workflow
            conf_dir(Path): path of folder with all .conf files for this workflow

        Returns:
            void
        """

        # extract values
        wf_name = wf_in.get_name()
        dag_file = wf_in.get_dag_definition_file()
        # get all files in conf_dir as string
        conf_file_list = []
        for file in conf_dir.iterdir():
            conf_file_list.append(str(file))
        # get all files in wf_in.__conf_folder
        other_file_list = []
        for file in wf_in.get_config_folder().iterdir():
            other_file_list.append(str(file))

        # check if workflow already exists
        workflow_exists_query = "SELECT name from Workflow WHERE name = %s"

        # raise exception if workflow name already exists
        if self.__databaseTable.check_for(workflow_exists_query, (wf_name,)):
            raise MatFlowException.InternalException(
                "ERROR: workflow '" + wf_name + "' already exists"
            )

        # create workflow entry
        workflow_query = "INSERT INTO Workflow (name, dag) VALUES (%s, %s)"
        self.__databaseTable.set(workflow_query, (wf_name, str(dag_file)))

        # create version entry
        version_query = (
            "INSERT INTO Version (wfName, version, note) VALUES (%s, %s, %s)"
        )
        self.__databaseTable.set(version_query, (wf_name, "1", ""))

        # get key of version number
        version_key = self.__get_key_of_workflow_version(wf_name, "1")

        # create all file entries for non-conf-files
        folderfile_query = "INSERT INTO FolderFile (wfName, file) VALUES (%s, %s)"
        for file_path in other_file_list:
            self.__databaseTable.set(folderfile_query, (wf_name, file_path))

        # create all file entries for conf-files
        conffile_set_query = "INSERT INTO ConfFile (file) VALUES (%s)"
        conffile_get_key_query = "SELECT confKey FROM ConfFile WHERE file = %s"
        versionfile_set_query = (
            "INSERT INTO VersionFile (versionID, filename, confKey) VALUES (%s, %s, %s)"
        )
        for file_path in conf_file_list:
            # injection into ConfFile
            self.__databaseTable.set(conffile_set_query, (file_path,))

            # get index of new entry; format into usable index
            # all names are unique in a workflow folder
            file_key = self.__databaseTable.get_one(
                conffile_get_key_query, (str(file_path),)
            )
            file_key = file_key[0]

            # injection into VersionFile
            filename = Path(file_path).name
            self.__databaseTable.set(
                versionfile_set_query, (version_key, filename, file_key)
            )

        # set active
        set_query = "INSERT INTO ActiveVersion (wfName, version) VALUES (%s, %s)"
        self.__databaseTable.set(set_query, (wf_name, "1"))

        return

    def get_names_of_workflows_and_config_files(self) -> Dict[str, List[str]]:
        """Return all Workflow names and the names of their corresponding config files.

        Extended description of function.

        Returns:
            Dict[str, List[Path]]: dictionary with workflow names as keys, and lists of Paths of config files as values

        """
        # define empty dictionary
        workflow_dict: Dict[str, List[str]] = {}
        # get all existing files with corresponding workflows
        query = "SELECT v.wfName, vf.filename FROM Version v INNER JOIN VersionFile vf ON vf.versionID = v.ID;"
        raw_data = self.__databaseTable.get_multiple(query, ())
        # build dictionary
        for (name, file_path) in raw_data:
            if name not in workflow_dict:
                workflow_dict[name] = [file_path]
            else:
                workflow_dict[name].append(file_path)

        return workflow_dict

    def create_new_version_of_workflow_instance(
        self, wf_name: str, new_version: DatabaseVersion, old_version_nr: str
    ):
        """Create a new Version of an existing Workflow with changed config Files.

        Args:
            wf_name(str): name of a workflow
            new_version(DatabaseVersion): NEW version number
            old_version_nr(str): version this one is based on

        Returns:
            void

        """
        # create new version entry
        new_version_nr = new_version.get_version_number().get_number()
        new_entry = "INSERT INTO Version (wfName, version) VALUES (%s, %s)"
        self.__databaseTable.set(new_entry, (wf_name, new_version_nr))
        # get keys of versions out of Version table
        new_version_index: str = self.__get_key_of_workflow_version(
            wf_name, new_version_nr
        )
        old_version_index: str = self.__get_key_of_workflow_version(
            wf_name, old_version_nr
        )

        # get all new file paths
        new_files = []
        for file in new_version.get_changed_config_files().iterdir():
            if file.is_file():
                new_files.append(file)

        # insert all new files into ConfFile
        file_insert = "INSERT INTO ConfFile (file) VALUES (%s)"
        get_file_key = "SELECT confKey FROM ConfFile WHERE file = %s"
        file_to_version = (
            "INSERT INTO VersionFile (versionID, filename, confKey) VALUES (%s,%s,%s)"
        )
        for file in new_files:
            # inject new file
            self.__databaseTable.set(file_insert, (str(file),))

            # get key from new file
            file_key = self.__databaseTable.get_one(get_file_key, (str(file),))
            file_key = file_key[0]

            # connect new file and new version
            self.__databaseTable.set(
                file_to_version, (new_version_index, file.name, file_key)
            )

        # connect old, not updated files of previous version
        # 'oldVersion' and 'newVersion' are used to get a better understanding of the query
        copy_old_files = (
            "INSERT INTO VersionFile (versionID, filename, confKey) SELECT newVersion, filename, "
            "confKey	FROM VersionFile	WHERE versionID = 'oldVersion'    AND filename    NOT IN ("
            "Select filename		FROM VersionFile        WHERE versionID = 'newVersion'); "
        )
        copy_old_files = copy_old_files.replace(
            "newVersion", str(new_version_index)
        ).replace("oldVersion", str(old_version_index))
        self.__databaseTable.set(copy_old_files, ())

    def get_config_file_from_workflow_instance(
        self, wf_name: str, conf_name: str, version: str
    ) -> Path:
        """Return single config file from a Workflow.

        Does NOT check if any of the values really exist.

        Args:
            wf_name(str): name of workflow
            conf_name(str): name of config file
            version(str): version identifier

        Returns:
            Path: searched conf File

        """
        # setup
        version_key = self.__get_key_of_workflow_version(wf_name, version)
        get_file_path_query = (
            "SELECT cf.file FROM VersionFile vf INNER JOIN ConfFile cf ON vf.confKey = cf.confKey "
            "WHERE versionID = %s AND  filename = %s "
        )

        # get path
        data = self.__databaseTable.get_one(
            get_file_path_query, (version_key, conf_name)
        )
        return Path(data[0])

    def get_config_file_from_active_workflow_instance(
        self, wf_name: str, conf_name: str
    ) -> Path:
        """Return single config file from active version of a Workflow.

        Args:
            wf_name(str): name of workflow
            conf_name(str): name of config file

        Returns:
            Path: conf File path

        """
        # NOTE: possible in one query, split up for intelligibility
        get_file_query = """SELECT cf.file 
                            FROM ConfFile cf INNER JOIN VersionFile vf 
                            ON cf.confKey = vf.confKey
                            WHERE versionID = %s
                            AND filename = %s
                            """
        # get version key
        active_version = self.get_active_version_of_workflow_instance(wf_name)
        active_version_key = self.__get_key_of_workflow_version(wf_name, active_version)

        file = self.__databaseTable.get_one(
            get_file_query, (active_version_key, conf_name)
        )

        return Path(file[0])

    # TODO Aufwendig
    def get_database_versions_of_workflow_instance(
        self, wf_name: str
    ) -> List[DatabaseVersion]:
        """Return all DatabaseVersions of a Workflow.

        Args:
            wf_name(str): name of workflow

        Returns:
            DatabaseVersion[]: all versions as DatabaseVersion objects

        """
        # different approach for version 1 and all following Versions:
        # 1) every file in version 1 is 'changed'
        get_version_one_files = """SELECT cf.file, v.note
                                             FROM (SELECT * 
                                                   FROM Version 
                                                   WHERE wfName = %s 
                                                   AND version = %s) v, VersionFile vf, ConfFile cf
                                             WHERE v.ID = vf.versionID 
                                             AND vf.confKey = cf.confKey
                                             """

        # 2) compare old and new version and get file path of new version file
        get_other_version_file = """SELECT v1.file, v1.note
                                    FROM (SELECT confKey, file
                                          FROM (SELECT * 
                                              FROM Version v
                                              WHERE wfName = %s
                                              AND version = %s) v, VersionFile vf, ConfFile cf
                                          WHERE v.ID = vf.versionID
                                          AND cf.confKey = vf.confKey) v1 LEFT JOIN
                                         (SELECT confKey
                                          FROM (SELECT * 
                                              FROM Version 
                                              WHERE wfName = %s
                                              AND version = %s) v, VersionFile vf
                                          WHERE v.ID = vf.versionID) v2 ON v1.confKey = v2.confKey
                                    WHERE NOT v1.confKey = v2.confKey
                                    """

        versions = self.get_version_numbers_of_workflow_instance(wf_name)
        database_versions: List[DatabaseVersion] = []  # return value
        for version in versions:
            version_number = VersionNumber(version)

            if version == "1":
                # get one file path and cut of the file name to get the path
                version_file = self.__databaseTable.get_one(
                    get_version_one_files, (wf_name, version)
                )

                # file -> (filepath, note)
                database_version = DatabaseVersion(
                    version_number,
                    version_file[1],
                    os.path.dirname(Path(version_file[0])),
                )
                database_versions.append(database_version)
                continue

            # else
            version_file = self.__databaseTable.get_one(
                get_other_version_file,
                (
                    wf_name,
                    version,
                    wf_name,
                    version_number.get_predecessor().get_number(),
                ),
            )

            # file -> (filepath, note)
            database_version = DatabaseVersion(
                version_number, version_file[1], os.path.dirname(Path(version_file[0]))
            )
            database_versions.append(database_version)

        return database_versions

    def set_active_version_through_number(self, wf_name: str, version: str):
        """Set the active version of a workflow in ActiveVersion table.
        Can insert new workflow + version into table

        Args:
            wf_name(str): name of workflow
            version(str): name of version to be set

        Returns:
            void

        """
        # check for valid wf_name and version
        check_query = "SELECT * FROM Version WHERE wfName=%s AND version=%s"
        if not self.__databaseTable.check_for(check_query, (wf_name, version)):
            raise MatFlowException.InternalException(
                "ERROR: Workflow '"
                + wf_name
                + "' and/or Version '"
                + version
                + "' does not exist"
            )

        # update ActiveVersion entry
        try:
            update_query = "UPDATE ActiveVersion SET version = %s WHERE wfName = %s"
            self.__databaseTable.modify(update_query, (version, wf_name))
        except MatFlowException.InternalException as err:
            # updating failed
            raise MatFlowException.InternalException(
                "ERROR: Can neither set or update active Version.\nMySQL ERROR:"
                + err.message
            )

        return

    def get_active_version_of_workflow_instance(self, wf_name: str) -> str:
        """Return Version of Workflow set as active.

        Args:
            wf_name(str): name of workflow

        Returns:
            str: active version identifier

        """
        get_query = "SELECT version FROM ActiveVersion WHERE wfName = %s"
        try:
            version_id = self.__databaseTable.get_one(get_query, (wf_name,))
        except MatFlowException.InternalException:
            raise MatFlowException.InternalException(
                "ERROR: workflow '{}' not found".format(wf_name)
            )

        return version_id[0]

    def get_version_numbers_of_workflow_instance(self, wf_name: str) -> List[str]:
        """Return all Versions of a workflow.

        Args:
            wf_name(str): name of workflow

        Returns:
            str[]: sorted list of versions

        """
        get_versions_query = "SELECT version FROM Version WHERE wfName = %s"
        raw_versions = self.__databaseTable.get_multiple(get_versions_query, (wf_name,))

        # raw_version is list of single tuples
        versions: List[str] = []
        for (version,) in raw_versions:
            versions.append(version)

        versions.sort(key=lambda x: list(map(int, x.split("."))))
        return versions


# TODO vvv delete before shipping vvv
def class_debugging():
    print("TEST IN WorkflowData START")
    print(
        "Comment out if not needed/crahses program because no Databaseconnection could be established"
    )

    wf_data = WorkflowData()
    # dummy data
    test_workflow1 = WorkflowInstance("workflow3", Path("./Testfile1.txt"), Path(""))
    test_workflow2 = WorkflowInstance(
        "workflow5", Path("./Testfile2.txt"), Path("../workflow")
    )
    try:
        wf_data.create_wf_instance(test_workflow1, Path(""))
    except MatFlowException.InternalException as err:
        print(err)
    try:
        wf_data.create_wf_instance(test_workflow2, Path("../workflow"))
    except MatFlowException.InternalException as err:
        print(err)

    dictionary = wf_data.get_names_of_workflows_and_config_files()
    print(dictionary)
    # retrieve dummy data
    # test = wfData.get_Server()
    # print(test)

    data = wf_data.get_active_version_of_workflow_instance("workflow3")
    print(data)

    versions = wf_data.get_version_numbers_of_workflow_instance("workflow3")
    print("Versions of workflow3")
    print(versions)

    conf_path = wf_data.get_config_file_from_workflow_instance(
        "workflow3", "mydb.conf", "1"
    )
    print(conf_path)

    print("TEST IN WorkflowData END!")


# class_debugging()
