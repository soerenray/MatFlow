from Implementierung.Database.DatabaseTable import DatabaseTable
from Implementierung.workflow.workflow_instance import WorkflowInstance
from pathlib import Path


class WorkflowData:
    __instance = None
    databaseTable = DatabaseTable.get_instance()

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
        #  get all files in conf_dir as string
        conf_file_list = []
        for file in conf_dir.iterdir():
            conf_file_list.append(str(file))
        print(conf_file_list)

        other_file_list = []
        for file in wf_in.get_config_folder().iterdir():
            other_file_list.append(str(file))
        print(other_file_list)

        # check if workflow already exists
        workflow_exists_query = "SELECT name from Workflow WHERE name = '{}'".format(wf_name)

        # TODO return exception
        # and return if workflow name already exists
        if self.databaseTable.check_for(workflow_exists_query):
            print("workflow already exists")
            return

        # create workflow entry
        workflow_query = "INSERT INTO Workflow (name, dag) VALUES ('{}', '{}')".format(wf_name, dag_file)
        self.databaseTable.set(workflow_query)

        # create version entry
        version_query = "INSERT INTO Version (wfName, version, note) VALUES ('{}', '{}', '{}')".format(wf_name, "1", "")
        self.databaseTable.set(version_query)

        # get key of version number
        get_version_key_query = "SELECT ID FROM Version WHERE wfName = '{}' AND version = '{}';".format(wf_name, "1")
        number = self.databaseTable.get(get_version_key_query)
        # number is ["(x,)"] and has to be made into x alone (x <= int)
        number = str(number[0]).replace('(', "").replace(')', "").replace(",", "")

        # create all file entries for non-conf-files
        folderfile_query = "INSERT INTO FolderFile (wfName, file) VALUES ('{}', '{}')"
        for file_path in other_file_list:
            self.databaseTable.set(folderfile_query.format(wf_name, file_path))

        # create all file entries for conf-files
        conffile_set_query = "INSERT INTO ConfFile (file) VALUES ('{}')"
        conffile_get_key_query = "SELECT confKey FROM ConfFile WHERE file = '{}'"
        versionfile_set_query = "INSERT INTO VersionFile (versionID, filename, confKey) VALUES ('{}', '{}', '{}')"
        for file_path in conf_file_list:
            # injection into ConfFile
            self.databaseTable.set(conffile_set_query.format(file_path))

            # get index of new entry & format into usable index
            # all names are unique in a workflow
            file_key = self.databaseTable.get(conffile_get_key_query.format(file_path))
            file_key = str(file_key[0]).replace('(', "").replace(')', "").replace(",", "")

            # injection into VersionFile
            filename = Path(file_path).name
            self.databaseTable.set(versionfile_set_query.format(number, filename, file_key))

        return

    # TODO return dictionary
    def get_Names_Of_Workflows_And_Config_Files(self):
        """Return all Worflow names and the names of their corresponding config files.

        Extended description of function.

        Returns:
            str[][]: of form <[workflow1; file11; file12;{...}],[workflow2, file21;{...}];{...}>

        """

    def create_New_Version_Of_Worlkflow_Instance(self, wfName, newVersion, oldVersionNr):
        """Create a new Version of an existing Workflow with changed config Files.

        Extended description of function.

        Args:
            wfName(str): name of a workflow
            newVersion(DatabaseVersion): NEW version number
            oldVersionNr(str): version this one is based on

        Returns:
            void

        """

    def get_Config_File_From_Workflow_Instance(self, wfName, confName, version):
        """Return single config file from a workflow.

        Extended description of function.

        Args:
            wfName(str): name of workflow
            confName(str): name of config file
            version(str): version identifier

        Returns:
            File: searched conf File

        """

    def get_Config_File_From_Active_Workflow_Instance(self, wfName, confName):
        """Return single config file from active version of a workflow.

        Extended description of function.

        Args:
            wfName(str): name of workflow
            confName(str): name of config file

        Returns:
            File: searched conf File

        """

    # TODO Aufwendig
    def get_Database_Versions_Of_Workflow_Instance(self, wfName):
        """Return all DatabaseVersions of a worflow.

        Extended description of function.

        Args:
            wfName(str): name of workflow

        Returns:
            DatabaseVersion[]: all versions as DatabaseVersion objects

        """

    def set_Active_Version_Through_Number(self, wfName, version):
        """Set the active version of a workflow.

        Extended description of function.

        Args:
            wfName(str): name of workflow
            version(str): name of version to be set

        Returns:
            void

        """

    def get_Active_Version_Of_Workflow_Instance(self, wfName):
        """Return workflow set as active in Database.

        Extended description of function.

        Args:
            wfName(str): name of workflow

        Returns:
            Workflow: Workflow object

        """

    def get_Version_Numbers_Of_Workflow_Instance(self, wfName):
        """Return all versions of a workflow.

        Extended description of function.

        Args:
            wfName(str): name of workflow

        Returns:
            str[]: sorted list of versions

        """


def class_debugging():
    print("TEST IN WorkflowData START")
    print("Comment out if not needed/crahses program because no Databaseconnection could be established")

    wfData = WorkflowData()
    # dummy data
    testworkflow = WorkflowInstance("workflow4", Path("./Testfile1.txt"), Path("."))
    data = wfData.create_wf_instance(testworkflow, Path("."))
    print(data)  # should be 'None'

    # retrieve dummy data
    # test = wfData.get_Server()
    # print(test)

    print("TEST IN WorkflowData END!")


# class_debugging()
