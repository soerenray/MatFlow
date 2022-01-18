import DatabaseTable
class WorkflowData:
    __instance = None

    @staticmethod
    def get_instance():
        if WorkflowData.__instance == None:
            WorkflowData()
        return WorkflowData.__instance

    def __init__(self):
        if WorkflowData.__instance != None:
            #throw exception
        else:
            WorkflowData.__instance = self


    def create_Workflow_Instance_From_Template(tName, wfName, confFold):


    def get_Names_Of_Workflows_And_Config_Files():


    def create_New_Version_Of_Worlkflow_Instance(wfName, newVersion, oldVersion):


    def get_Config_File_From_Workflow_Instance(wfName, confName):


    def get_Database_Versions_Of_Workflow_Instance(wfName):


    def set_Active_Version_Through_Number(wfName, version):


    def get_Database_Versions_Of_Workflow_Instance(wfName):


    def get_Version_Numbers_Of_Workflow_Instance(wfName):



