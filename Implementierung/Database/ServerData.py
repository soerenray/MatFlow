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
        """Write new Server into database.

        Throw error if ip already exists.

        Args:
            server(Server): new server

        Returns:
            void

        """


    def get_Server():
        """Get server in database.

        NOTE:   Currently there is no intention of storing multiple servers to connect to,
                as such, no argument is needed to get the one(1) that is in the database


        Returns:
            Server: server from database

        """