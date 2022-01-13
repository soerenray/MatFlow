class WorkflowManager():
    __instance = None

    def __init__(self):
        raise Error("Call get_frontend_api())

    @classmethod
    def get_instance(self):
        if self.__instance is None:
            print('Creating new instance')
            self.__instance = self.__new__(self)
            # Put any initialization here.
        return self.__instance
