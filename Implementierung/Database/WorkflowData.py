from Implementierung.Database.DatabaseTable import DatabaseTable
from Implementierung.workflow.workflow_instance import WorkflowInstance
from Implementierung.workflow.database_version import DatabaseVersion
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

    def create_wf_instance(self, wf_in: WorkflowInstance, conf_dir: Path):
        # TODO replace values to
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

        # TODO return exception
        # and return if workflow name already exists
        if self.__databaseTable.check_for(workflow_exists_query):
            print("workflow already exists")
            return

        # create workflow entry
        workflow_query = "INSERT INTO Workflow (name, dag) VALUES ('{}', '{}')".format(wf_name, dag_file)
        self.__databaseTable.set(workflow_query)

        # create version entry
        version_query = "INSERT INTO Version (wfName, version, note) VALUES ('{}', '{}', '{}')".format(wf_name, "1", "")
        self.__databaseTable.set(version_query)

        # get key of version number
        get_version_key_query = "SELECT ID FROM Version WHERE wfName = '{}' AND version = '{}';".format(wf_name, "1")
        number = self.__databaseTable.get(get_version_key_query)
        # number is ["(x,)"] and has to be made into x alone (x <= int)
        number = str(number[0]).replace('(', "").replace(')', "").replace(",", "")

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
            file_key = self.__databaseTable.get(conffile_get_key_query.format(file_path))
            file_key = str(file_key[0]).replace('(', "").replace(')', "").replace(",", "")

            # injection into VersionFile
            filename = Path(file_path).name
            self.__databaseTable.set(versionfile_set_query.format(number, filename, file_key))

        return

    def get_names_of_workflows_and_config_files(self) -> Dict[str, List[Path]]:
        """Return all Workflow names and the names of their corresponding config files.

        Extended description of function.

        Returns:
            Dict[str, List[Path]]: dictionary with workflow names as keys, and lists of Paths of config files as values

        """
        # define empty dictionary
        workflow_dict: Dict[str, List[Path]] = {}
        # get all existing files with corresponding workflows
        query = "SELECT v.wfName, vf.filename FROM Version v INNER JOIN VersionFile vf ON vf.versionID = v.ID;"
        raw_data = self.__databaseTable.get(query)
        print("start dictionary print")
        print(raw_data)
        # build dictionary
        for (name, file_path) in raw_data:
            if name not in workflow_dict:
                workflow_dict[name] = [Path(file_path)]
            else:
                workflow_dict[name].append(Path(file_path))
            print("key: " + name + "; value: " + str(file_path))

        return workflow_dict

    def create_new_version_of_workflow_instance(self, wf_name: str, new_version: DatabaseVersion, old_version_nr: str):
        """Create a new Version of an existing Workflow with changed config Files.

        Extended description of function.

        Args:
            wf_name(str): name of a workflow
            new_version(DatabaseVersion): NEW version number
            old_version_nr(str): version this one is based on

        Returns:
            void

        """

    def get_config_file_from_workflow_instance(self, wf_name: str, conf_name: str, version: str):
        """Return single config file from a Workflow.

        Extended description of function.

        Args:
            wf_name(str): name of workflow
            conf_name(str): name of config file
            version(str): version identifier

        Returns:
            File: searched conf File

        """

    def get_config_file_from_active_workflow_instance(self, wf_name: str, conf_name: str):
        """Return single config file from active version of a Workflow.

        Extended description of function.

        Args:
            wf_name(str): name of workflow
            conf_name(str): name of config file

        Returns:
            File: searched conf File

        """

    # TODO Aufwendig
    def get_database_versions_of_workflow_instance(self, wf_name: str):
        """Return all DatabaseVersions of a Workflow.

        Extended description of function.

        Args:
            wf_name(str): name of workflow

        Returns:
            DatabaseVersion[]: all versions as DatabaseVersion objects

        """

    def set_active_version_through_number(self, wf_name: str, version: str):
        """Set the active version of a workflow.

        Extended description of function.

        Args:
            wf_name(str): name of workflow
            version(str): name of version to be set

        Returns:
            void

        """

    def get_active_version_of_workflow_instance(self, wf_name: str):
        """Return Workflow set as active in Database.

        Extended description of function.

        Args:
            wf_name(str): name of workflow

        Returns:
            Workflow: Workflow object

        """

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
    test_workflow1 = WorkflowInstance("workflow1", Path("./Testfile1.txt"), Path("."))
    test_workflow2 = WorkflowInstance("workflow2", Path("./Testfile2.txt"), Path("./../workflow"))
    wf_data.create_wf_instance(test_workflow1, Path("."))
    wf_data.create_wf_instance(test_workflow2, Path("./../workflow"))

    wf_data.get_names_of_workflows_and_config_files()

    # retrieve dummy data
    # test = wfData.get_Server()
    # print(test)

    print("TEST IN WorkflowData END!")


if __name__ == '__main__':
    class_debugging()
