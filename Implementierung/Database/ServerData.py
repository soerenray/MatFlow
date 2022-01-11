class ServerData:
    __instance = None

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
