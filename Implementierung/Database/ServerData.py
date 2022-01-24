import DatabaseTable
class ServerData:
    __instance = None
    databaseTable = DatabaseTable.DatabaseTable.get_instance()


    @staticmethod
    def get_instance():
        if ServerData.__instance == None:
            ServerData()
        return ServerData.__instance

    def __init__(self):
        if ServerData.__instance != None:
            #throw exception
            a = 12
        else:
            ServerData.__instance = self

    def write_Server(self, server):
        """Write new Server into database.

        Throw error if ip already exists.

        Args:
            server(Server): new server

        Returns:
            void
        """


    def get_Server(self):
        """Get server in database.

        NOTE:   Currently there is no intention of storing multiple servers to connect to,
                as such, no argument is needed to get the one(1) that is in the database

        Returns:
            string[]: 2-element list with format [<IP>,<Name>]
        """
        query = "SELECT * FROM Server;"
        data = self.databaseTable.get(query)
        if not data:
            #throw exception no entry
            return data

        return data



def class_debugging():
    print("TEST IN ServerData START")
    print("Comment out if not needed/crahses program because no Databaseconnection could be established")


    sData = ServerData()
    test = sData.get_Server()
    print(test)


    print("TEST IN ServerData END!")

class_debugging()
