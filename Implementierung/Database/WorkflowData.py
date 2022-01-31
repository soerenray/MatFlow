from Implementierung.ExceptionPackage import MatFlowException
from Implementierung.Database.DatabaseTable import DatabaseTable
from Implementierung.workflow.workflow_instance import WorkflowInstance
from Implementierung.workflow.database_version import DatabaseVersion
from pathlib import Path
from typing import Dict, List
import re


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
        """ Returns: index of workflow version"""
        get_version_key_query = "SELECT ID FROM Version WHERE wfName = '{}' AND version = '{}';".format(wf_name,
                                                                                                        version)
        version_key = self.__databaseTable.get_one(get_version_key_query)
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
        workflow_exists_query = "SELECT name from Workflow WHERE name = '{}'".format(wf_name)

        # raise exception if workflow name already exists
        if self.__databaseTable.check_for(workflow_exists_query):
            raise MatFlowException.InternalException("ERROR: workflow " + wf_name + " already exists")

        # create workflow entry
        workflow_query = "INSERT INTO Workflow (name, dag) VALUES ('{}', '{}')".format(wf_name, dag_file)
        self.__databaseTable.set(workflow_query)

        # create version entry
        version_query = "INSERT INTO Version (wfName, version, note) VALUES ('{}', '{}', '{}')".format(wf_name, "1", "")
        self.__databaseTable.set(version_query)

        # get key of version number
        version_key = self.__get_key_of_workflow_version(wf_name, "1")

        # create all file entries for non-conf-files
        folderfile_query = "INSERT INTO FolderFile (wfName, file) VALUES ('{}', '{}')"
        for file_path in other_file_list:
            self.__databaseTable.set(folderfile_query.format(wf_name, file_path))

        # create all file entries for conf-files
        conffile_set_query = "INSERT INTO ConfFile (file) VALUES ('{}')"
        conffile_get_key_query = "SELECT confKey FROM ConfFile WHERE file = '{}'"
        versionfile_set_query = "INSERT INTO VersionFile (versionID, filename, confKey) VALUES ('{}', '{}', '{}')"
        for file_path in conf_file_list:
            # injection into ConfFile
            self.__databaseTable.set(conffile_set_query.format(file_path))

            # get index of new entry; format into usable index
            # all names are unique in a workflow folder
            file_key = self.__databaseTable.get_one(conffile_get_key_query.format(file_path))
            file_key = file_key[0]

            # injection into VersionFile
            filename = Path(file_path).name
            self.__databaseTable.set(versionfile_set_query.format(version_key, filename, file_key))

        # set active
        self.set_active_version_through_number(wf_name, "1")

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
        raw_data = self.__databaseTable.get_multiple(query)
        # build dictionary
        for (name, file_path) in raw_data:
            if name not in workflow_dict:
                workflow_dict[name] = [file_path]
            else:
                workflow_dict[name].append(file_path)

        return workflow_dict

    # TODO Revision/Testing needed: 'worked' first try, something's wrong!
    def create_new_version_of_workflow_instance(self, wf_name: str, new_version: DatabaseVersion, old_version_nr: str):
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
        new_entry = "INSERT INTO Version (wfName, version) VALUES ('{}', '{}')"
        new_entry = new_entry.format(wf_name, new_version_nr)
        self.__databaseTable.set(new_entry)
        # get keys of versions out of Version table
        new_version_index = self.__get_key_of_workflow_version(wf_name, new_version_nr)
        old_version_index = self.__get_key_of_workflow_version(wf_name, old_version_nr)

        # get all new file paths
        new_files = []
        for file in new_version.get_changed_config_files().iterdir():
            if file.is_file():
                new_files.append(file)

        # insert all new files into ConfFile
        file_insert = "INSERT INTO ConfFile (file) VALUES ('{}')"
        get_file_key = "SELECT confKey FROM ConfFile WHERE file = '{}'"
        file_to_version = "INSERT INTO VersionFile (versionID, filename, confKey) VALUES ({},'{}',{})"
        for file in new_files:
            # inject new file
            file_insert_local = file_insert.format(str(file))
            self.__databaseTable.set(file_insert_local)

            # get key from new file
            get_file_key_local = get_file_key.format(str(file))
            file_key = self.__databaseTable.get_one(get_file_key_local)
            file_key = file_key[0]

            # connect new file and new version
            file_to_version_local = file_to_version.format(new_version_index, file.name, file_key)
            self.__databaseTable.set(file_to_version_local)

        # connect old, not updated files of previous version
        # query is also saved as 'copy old not updated files -query.txt'
        copy_old_files = "INSERT INTO VersionFile (versionID, filename, confKey) SELECT newVersion, filename, " \
                         "confKey	FROM VersionFile	WHERE versionID = 'oldVersion'    AND filename    NOT IN (" \
                         "Select filename		FROM VersionFile        WHERE versionID = 'newVersion'); "
        copy_old_files = copy_old_files.replace("newVersion", new_version_index).replace("oldVersion",
                                                                                         old_version_index)
        self.__databaseTable.set(copy_old_files)

    def get_config_file_from_workflow_instance(self, wf_name: str, conf_name: str, version: str) -> Path:
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
        get_file_path_query = "SELECT cf.file FROM VersionFile vf INNER JOIN ConfFile cf ON vf.confKey = cf.confKey " \
                              "WHERE versionID = '{}' AND  filename = '{}' "
        get_file_path_query = get_file_path_query.format(version_key, conf_name)

        # get path
        data = self.__databaseTable.get_one(get_file_path_query)
        return Path(data[0])

    # TODO Implementierung
    def get_config_file_from_active_workflow_instance(self, wf_name: str, conf_name: str) -> Path:
        """Return single config file from active version of a Workflow.

        Extended description of function.

        Args:
            wf_name(str): name of workflow
            conf_name(str): name of config file

        Returns:
            Path: searched conf File

        """

    # TODO Aufwendig
    def get_database_versions_of_workflow_instance(self, wf_name: str) -> List[DatabaseVersion]:
        """Return all DatabaseVersions of a Workflow.

        Extended description of function.

        Args:
            wf_name(str): name of workflow

        Returns:
            DatabaseVersion[]: all versions as DatabaseVersion objects

        """

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
        check_query = "SELECT * FROM Version WHERE wfName='{}' AND version='{}'"
        check_query = check_query.format(wf_name, version)
        if not self.__databaseTable.check_for(check_query):
            raise MatFlowException.InternalException("ERROR: Workflow '" + wf_name + "'/Version '" + version +
                                                     "' does not exist")

        # update ActiveVersion entry
        try:
            update_query = "UPDATE ActiveVersion SET version = '{}' WHERE wfName = '{}"
            update_query = update_query.format(version, wf_name)
            self.__databaseTable.modify(update_query)
        except MatFlowException.InternalException:
            try:
                # chance that workflow is only just created and has no valid entry in ActiveVersion
                set_query = "INSERT INTO ActiveVersion (wfName, version) VALUES ('{}', '{}')"
                set_query = set_query.format(wf_name, version)
                self.__databaseTable.set(set_query)
            except MatFlowException.InternalException as err:
                # updating and inserting failed
                raise MatFlowException.InternalException("ERROR: Can neither set or update active Version.\n" +
                                                         "MySQL ERROR:" + err.message)
        return

    def get_active_version_of_workflow_instance(self, wf_name: str) -> str:
        """Return Version of Workflow set as active.

        Args:
            wf_name(str): name of workflow

        Returns:
            str: active version identifier

        """
        get_query = "SELECT version FROM ActiveVersion WHERE wfName = '{}'"
        get_query = get_query.format(wf_name)
        try:
            version_id = self.__databaseTable.get_one(get_query)
        except MatFlowException.InternalException:
            raise MatFlowException.InternalException("ERROR: workflow '{}' not found".format(wf_name))

        return version_id[0]

    # TODO Implementierung
    def get_version_numbers_of_workflow_instance(self, wf_name: str):
        """Return all Versions of a workflow.

        Extended description of function.

        Args:
            wf_name(str): name of workflow

        Returns:
            str[]: sorted list of versions

        """


def class_debugging():
    print("TEST IN WorkflowData START")
    print("Comment out if not needed/crahses program because no Databaseconnection could be established")

    wf_data = WorkflowData()
    # dummy data
    test_workflow1 = WorkflowInstance("workflow3", Path("./Testfile1.txt"), Path("."))
    test_workflow2 = WorkflowInstance("workflow5", Path("./Testfile2.txt"), Path("./../workflow"))
    try:
        wf_data.create_wf_instance(test_workflow1, Path("."))
    except MatFlowException.InternalException as err:
        print(err)
    try:
        wf_data.create_wf_instance(test_workflow2, Path("./../workflow"))
    except MatFlowException.InternalException as err:
        print(err)

    dictionary = wf_data.get_names_of_workflows_and_config_files()
    print(dictionary)
    # retrieve dummy data
    # test = wfData.get_Server()
    # print(test)

    data = wf_data.get_active_version_of_workflow_instance("workflow3")
    print(data)

    conf_path = wf_data.get_config_file_from_workflow_instance("workflow3", "mydb.conf", "1")
    print(conf_path)

    print("TEST IN WorkflowData END!")


# class_debugging()
