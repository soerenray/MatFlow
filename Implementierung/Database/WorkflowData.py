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

    def create_wf_instance(self, wf_name, dag_file):
        # TODO replace values to    wf_in: WorkflowInstance, conf_dir: Path
        """Create a new instance of a workflow by using the dag-File of a Template with the Version set to 1.

        Extended description of function.

        Args:
            t_name(str): name of template
            wf_name(str): NEW name of a workflow
            confFold(str[]): paths of the config-folder files

        Returns:
            void
        """
        # check if workflow already exists
        workflow_exists_query = "SELECT name from Workflow WHERE name = '{}'".format(wf_name)
        # TODO return exception
        # and return if workflow name already exists
        if not self.databaseTable.check_for(workflow_exists_query):
            print("checkpoint1")
            return

        # create workflow entry
        workflow_query = "INSERT INTO Workflow (name, dag) VALUES ('{}', '{}')".format(wf_name, dag_file)
        self.databaseTable.set(workflow_query)
        # create version entry
        version_query = "INSERT INTO Version (wfName, version, note) VALUES ('{}', '{}', '{}')".format(wf_name, "1", "")
        self.databaseTable.set(version_query)

        # get key of version number
        get_version_key_query = "SELECT ID FROM Version WHERE wfName = '{}' AND version = '{}';".format(wf_name, "1")
        number = self.databaseTable.get(get_version_key_query)[0]
        print("Index is " + number + "!")

        # TODO continue implementation

        # execute
        # data = self.databaseTable.set(query)
        return data

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
    data = wfData.create_wf_instance("workflowName3", "dag1 filepath")
    print(data)  # should be 'None'

    # retrieve dummy data
    # test = wfData.get_Server()
    # print(test)

    print("TEST IN WorkflowData END!")


#class_debugging()
