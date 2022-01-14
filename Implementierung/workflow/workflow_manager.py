class WorkflowManager():
    # exceptions are missing TODO
    # swap out "file" for real class
    __instance = None

    def __init__(self):
        raise Error("Call get_instance())

    @classmethod
    def get_instance(self) -> WorkflowManager:
        """Returns the singleton object of the WorkflowManager class.

            Returns the singleton object if already existing otherwise calls the private constructor.

            Returns:
                WorkflowManager: singleton object

            """
        if self.__instance is None:
            print('Creating new instance')
            self.__instance = self.__new__(self)
            # Put any initialization here.
        return self.__instance

    def create_template(self, template: Template):
        """Causes the creation of a new template entry in the database.

        Fails if the Template.name is already occuring in the database.
        In case of success the new template can be used for creating workflow instances afterwards.

        Args:
            template (Template): Template object that provides all necessery information for creating
            a new workflow template.

        """

    def create_workflow_instance_from_template(self, template_name: str, workflow_instance_name: str, config_files):
        # type of config_files TODO
        """Causes the instantiation of a workflow instance under the use of a workflow template.

        Extended description of function. TODO

        Args:
            template_name (str): The identifier of the template that is used for instantiation
            workflow_instance_name (str): The name of the new workflow instance
            config_files (): Cointains all the files needed for the execution of the workflow

        """

    def get_dag_representation_from_template(self, template:Template)->file:
        """Takes a dag file and a dag name and returns a preview of the defined graph

        Uses functionality of airflow. Is used in the template editor of the client application.

        Args:
            template (Template): The template dag to represent

        Returns:
            file: Image with visual representation of the given dag

        """
        return None

    def get_template_names(self)-> :
        #TODO return type
        """Returns the names of all templates.

        Makes database request and returns the names of all templates in the system.

        Returns:
            ?: Collection of all template names

        """
        return None

    def get_template_from_name(self, template_name: str)->Template:
        """Returns template idetified by the given name.

        Forwards the request for the named template to the database and returns result.

        Args:
            template_name (str): The identifier of the desired template

        Returns:
            Template: Desired template

        """
        return None

    def get_names_of_workflows_and_config_files(self)->:
        # TODO return type
        """Returns the names of all workflow instances aswell as the names of the associated config-files

        Forwards the request to the database.


        Returns:
            ?: A two-dimensional array where the innner arrays start with the name of the template which is followed by
                the names of the associated config-files

        """
        return None

    def get_key_value_pairs_from_config_file(self, workflow_instance_name: str, config_file_name: string)->]:
        # TODO return type
        """Returns the collection of all key value pairs in the specified config-file.

        Requests the desired config-file from the current version of the named workflow instance from the database.
        Afterwards changes the format from a file into an array of key-value-pairs and returns the result.


        Args:
            workflow_instance_name (str): The identifier of the workflow instance the config file is attached to
            config_file_name (str): The name of the desired config file

        Returns:
            ?: A collection of key value pairs

        """
        return None

    def create_new_version_of_workflow_instance(self, workflow_instance_name: str, changed_files: , version_note:str):
        # TODO type of param "changed_files"
        """Causes the creation of a new version of the workflow instance in the database.

        The new version is obtained by overwriting the given changed files and adopting all other files of the
        predecessor version. The predecessor of the new version is the active version of the instance.

        Args:
            workflow_instance_name (str): The identifier of the workflow instance of which a new version is created
            changed_files (?): The config-files that were changed in comparison to the predecessor version
                in key-value-pair representation
            version_note (str): Note about the new version given by the user

        """
        return None

    def set_active_version_through_number(self, workflow_instance_name: str, version_number: str):
        """Changes the active version of a workflow instance in the database.

        Before requesting the change in the database a call to the airflow api is made to make sure the workflow
        instance isn't currently running.

        Args:
            workflow_instance_name (str): The name of the workflow instance of which the active version shall be changed
            version_number (str): The number of the new active version

        """


