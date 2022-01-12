class JSONToPython():

    """
    This class converts all json data into the wanted object by extracting certain keys and values and
    instantiating a new (temporary) object which executes the wanted methods (e.g. extract server and
    then execute set new container limit). Instantiated objects will be deleted by the garbage collection
    after they are finished writing back / getting data from the database.
    """
    @staticmethod
    def extract_user(json_details: str) -> User:
        """
        extracts json details and builds a new User based off of these json details

        Args:
            json_details(String): contains encoded user

        Returns:
            User: decoded user object
        """
        pass

    @staticmethod
    def extract_server(json_details: str) -> Server:
        """
        extracts json details and builds a new Server based off of these json details

        Args:
            json_details(String): contains encoded server

        Returns:
            Server: decoded server object
        """
        pass

    @staticmethod
    def extract_template(json_details: str) -> Template:
        """
        extracts json details and builds a new Template based off of these json details

        Args:
            json_details(String): contains encoded template

        Returns:
            Template: decoded template object
        """
        pass

    @staticmethod
    def extract_configs(json_details: str) -> ReducedConfigFile:
        """
        extracts json details and builds a new ReducedConfigFile array based off of these json details

        Args:
            json_details(String): contains encoded reduced config files

        Returns:
            ReducedConfigFile[]: array of reduced config files
        """
        #hier array von ReducedConfigFile
        pass

