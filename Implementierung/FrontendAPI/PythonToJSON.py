from __future__ import annotations

class PythonToJSON():

    """
    This class converts all python objects into json data by extracting certain keys and values and dumping them
    into a json object.
    """

    @staticmethod
    def encode_user(user: User) -> str:
        """
        extracts all user attributes and dumps them into json object

        Args:
            user(User): user whose attributes are to be encoded

        Returns:
            String: json-dumped object containing encoded user
        """
        pass

    @staticmethod
    def extract_server(server: Server) -> str:
        """
        extracts all server attributes and dumps them into json object

        Args:
            server(Server): server whose attributes are to be encoded

        Returns:
            String: json-dumped object containing encoded server
        """
        pass

    @staticmethod
    def encode_template(template: Template) -> str:
        """
        extracts all template attributes and dumps them into json object

        Args:
            template(Template): template whose attributes are to be encoded

        Returns:
            String: json-dumped object containing encoded template
        """
        pass

    @staticmethod
    def encode_wf_instance(wf_instance: WorkflowInstance) -> str:
        """
        extracts all workflow instance attributes and dumps them into json object

        Args:
            wf_instance(WorkflowInstance): workflow instance whose attributes are to be encoded

        Returns:
            String: json-dumped object containing encoded workflow instance
        """
        pass

    @staticmethod
    def encode_config(reduced_config: ReducedConfigFile) -> str:
        """
        extracts all reduced_config attributes and dumps them into json object

        Args:
            reduced_config(ReducedConfigFile): reduced config file whose attributes are to be encoded

        Returns:
            String: json-dumped object containing encoded reduced config file (essentially key value pairs)
        """
        pass

    @staticmethod
    def encode_versions(versions: list[Version]) -> str:
        """
        extracts all version attributes of each version and dumps them into one json object
        Args:
            versions(Version[]): array of versions whose attributes are to be encoded

        Returns:
            String: json-dumped object containing encoded versions
        """
        pass