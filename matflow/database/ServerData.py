from matflow.database.DatabaseTable import DatabaseTable
from matflow.hardwareadministration.Server import Server
from typing import List, Tuple


class ServerData:
    __instance = None
    databaseTable = DatabaseTable.get_instance()

    @staticmethod
    def get_instance():
        if ServerData.__instance is None:
            ServerData()
        return ServerData.__instance

    def __init__(self):
        if ServerData.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ServerData.__instance = self

    def write_server(self, server: Server):
        """Write new Server into database.

        Args:
            server(Server): new server

        Returns:
            void
        """
        # get values
        name = server.getName()
        ip_address = server.getAddress()

        # insert values
        query = "INSERT INTO Server (ip, name) VALUES (%s, %s)"
        # execute
        self.databaseTable.set(query, (ip_address, name))
        return

    def get_server(self) -> List[Tuple[str, str]]:
        """Get server in database.

        NOTE:   Currently there is no intention of storing multiple servers to connect to,
                as such, no argument is needed to get the one(1) that is in the database.
                If no entry exists, the return value is []
                If one entry exists, the return value is [<IP>,<Name>]
                If two or more entries exist, the return value is [(<IP>,<Name>), (<IP>,<Name>), ...]

        Returns:
            string[]: 2-element list with format [<IP>,<Name>]
        """
        query = "SELECT * FROM Server;"  # get all entries
        data = self.databaseTable.get(query)
        if not data:
            # throw exception no entry?
            return data

        return data


# TODO vvv delete before shipping vvv
def class_debugging():
    print("TEST IN ServerData START")
    print(
        "Comment out if not needed/crahses program because no Databaseconnection could be established"
    )

    s_data = ServerData()
    # dummy data
    server = Server("name1", "adress1", "status1", 42, True, ["no", "limit"])
    s_data.write_server(server)

    # retrieve dummy data
    test = s_data.get_server()
    print(test)

    print("TEST IN ServerData END!")


# class_debugging()
