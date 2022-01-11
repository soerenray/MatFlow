class DatabaseData:
    __instance = None

    @staticmethod
    def get_instance():
        if DatabaseData.__instance == None:
            DatabaseData()
        return DatabaseData.__instance

    def __init__(self):
        if DatabaseData.__instance != None:
            #throw exception
        else:
            DatabaseData.__instance = self