from Implementierung.Database.DatabaseTable import DatabaseTable
class WorkflowData:
    __instance = None

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


    def create_Workflow_Instance_From_Template(self, tName, wfName, confFold):
        """Create a new instance of a worflow by using the dag-File of a Template with the Version set to 1.

        Extended description of function.

        Args:
            tName(str): name of template
            wfName(str): NEW name of a workflow
            confFold(): files of the config-folder

        Returns:
            void

        """


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


