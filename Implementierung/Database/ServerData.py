import DatabaseTable
class ServerData:
    __instance = None
    databaseTable = DatabaseTable.get_instance()


    @staticmethod
    def get_instance():
        if ServerData.__instance == None:
            ServerData()
        return ServerData.__instance

    def __init__(self):
        if ServerData.__instance != None:
            #throw exception
        else:
            ServerData.__instance = self

    def write_Server(server):


    def get_Server():
