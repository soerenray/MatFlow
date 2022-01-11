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