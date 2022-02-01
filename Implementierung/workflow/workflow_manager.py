import errno
import os
import requests
import shutil
from pathlib import Path
from typing import List, Tuple, Dict
from .frontend_version import FrontendVersion
from .database_version import DatabaseVersion
from .template import Template
from .reduced_config_file import ReducedConfigFile
from .config_file import ConfigFile
from .version_number import VersionNumber
from Implementierung.workflow.workflow_instance import WorkflowInstance
from Implementierung.ExceptionPackage.MatFlowException import DoubleTemplateNameException, InternalException, \
    DoubleWorkflowInstanceNameException
from Implementierung.Database.TemplateData import TemplateData
from Implementierung.Database.WorkflowData import WorkflowData


class WorkflowManager:
    """
    This class provides a singleton object that receives all requests addressed to this package.
    This class is also communicating with the API of Airflow as well as with the Database package.
    """
    # exceptions are missing TODO
    __instance = None
    __template_data: TemplateData = TemplateData.get_instance()
    __workflow_data: WorkflowData = WorkflowData.get_instance()
    __versions_base_directory: Path = Path("")  # TODO
    __template_base_directory: Path = Path("")  # TODO
    __airflow_dag_folder: Path = Path("")  # TODO
    __airflow_address: str = "http://localhost:8080/"  # TODO
    __initial_version_note = "initial version"

    def __init__(self):
        raise Exception("Call get_instance()")

    @classmethod
    def get_instance(cls):
        """Returns the singleton object of the WorkflowManager class.

            Returns the singleton object if already existing otherwise calls the private constructor.
            """
        if cls.__instance is None:
            # Creating new instance
            cls.__instance = cls.__new__(cls)
        return cls.__instance

    def create_template(self, template: Template):
        """Causes the creation of a new template entry in the database.

        Fails if the Template.name is already occurring in the database.
        In case of success the new template can be used for creating workflow instances afterwards.

        Args:
            template (Template): Template object that provides all necessary information for creating
            a new workflow template.

        Raises:
            DoubleTemplateNameException: If the name of the given template isn't a valid identifier

        """
        # make sure the template name wasn't used before
        if template.get_name() + ".py" in os.listdir(self.__template_base_directory):
            raise DoubleTemplateNameException("")

        # now safe the new dag definition file in the template folder
        new_path: Path = self.__template_base_directory / (template.get_name() + ".py")
        shutil.copy(template.get_dag_definition_file(), new_path)

        # maybe make the file ro TODO

        # adjust the attribute of the template
        template.set_dag_definition_file(new_path)

    def create_workflow_instance_from_template(
            self, template_name: str, workflow_instance_name: str, config_files: Path):
        """Causes the instantiation of a workflow instance under the use of a workflow template.

        Args:
            template_name (str): The identifier of the template that is used for instantiation
            workflow_instance_name (str): The name of the new workflow instance
            config_files (Path): Contains all the files needed for the execution of the workflow

        """
        # get the template object corresponding to the name
        template_path: Path = self.__template_base_directory / (template_name + ".py")
        if not os.path.isfile(template_path):
            raise InternalException("Internal Error: " + template_name + " isn't a known template name.")
        template: Template = Template(template_name, template_path)

        # check if the workflow_instance_name is already used
        existing_names: List[str] = os.listdir(self.__versions_base_directory)
        if workflow_instance_name in existing_names:  # otherwise, the name is a valid identifier
            raise DoubleWorkflowInstanceNameException("")

        # try to create a WorkflowInstance object
        workflow_instance: WorkflowInstance = WorkflowInstance(
            workflow_instance_name, template.get_dag_definition_file(), config_files)  # maybe EmptyDagFolderException

        # now we create a new directory for the instance
        instance_path: Path = self.__versions_base_directory / workflow_instance_name
        os.mkdir(instance_path)
        # dag_path: Path = instance_path / (template_name + ".py")
        shutil.copy(template.get_dag_definition_file(), instance_path)  # copy dag definition file

        # under that dir we create another called "current_conf" that contains all files for the execution
        # the version of the file always matches the current version of the wf instance
        current_conf_path: Path = instance_path / "current_conf"
        self.__copy_files_with_extension(config_files, current_conf_path, "")

        # also, one dir for the initial version that contains only the '.conf'-files
        version_path: Path = instance_path / "1"
        self.__copy_files_with_extension(config_files, version_path, ".conf")

        # update the conf-dir-path of the workflow instance to the permanent location
        # + make a request to the database to add the new instance
        workflow_instance.set_config_folder(current_conf_path)
        self.__workflow_data.create_wf_instance(workflow_instance, version_path)

        # overwrite dag_id in the dag definition file + add  it to the airflow dag folder
        workflow_instance.activate_instance(self.__airflow_dag_folder)
        # TODO -> write "activate_instance" in WorkflowInstance

    def get_dag_representation_from_template(self, template: Template) -> Path:
        """Takes a dag file and a dag name and returns a preview of the defined graph

        Uses functionality of airflow. Is used in the template editor of the client application.

        Args:
            template (Template): The template dag to represent

        Returns:
            Path: Image with visual representation of the given dag

        """
        return Path("workflow/tests/dummy_dag.png")  # TODO this is only a dummy implementation

    def get_template_names(self) -> List[str]:
        """Returns the names of all templates.

        Makes database request and returns the names of all templates in the system.

        Returns:
            List[str]: Collection of all template names

        """
        file_names: List[str] = os.listdir(self.__template_base_directory)  # still has name extensions
        return [os.path.splitext(file_name)[0] for file_name in file_names]  # removed extensions

    def get_template_from_name(self, template_name: str) -> Template:
        """Returns template identified by the given name.

        Forwards the request for the named template to the database and returns result.

        Args:
            template_name (str): The identifier of the desired template

        Returns:
            Template: Desired template

        """
        if not os.listdir(self.__template_base_directory).__contains__(template_name + ".py"):
            raise InternalException("Internal Error: Selected template: " + template_name + " doesn't exist.")
        # otherwise, the template is available
        template_path: Path = self.__template_base_directory / (template_name + ".py")
        return Template(template_name, template_path)

    def get_names_of_workflows_and_config_files(self) -> Dict[str, List[str]]:
        """Returns the names of all workflow instances as well as the names of the associated config-files

        Forwards the request to the database.

        Returns:
            List[List[str]]: A two-dimensional array where the inner arrays start with the name of the template which
            is followed by the names of the associated config-files

        """
        return self.__workflow_data.get_names_of_workflows_and_config_files()

    def get_key_value_pairs_from_config_file(
            self, workflow_instance_name: str, config_file_name: str) -> ReducedConfigFile:
        """Returns the collection of all key value pairs in the specified config-file.

        Requests the desired config-file from the current version of the named workflow instance from the database.
        Afterwards changes the format from a file into an array of key-value-pairs and returns the result.


        Args:
            workflow_instance_name (str): The identifier of the workflow instance the config file is attached to
            config_file_name (str): The name of the desired config file

        Returns:
            List[Tuple[str, str]]: The list of key value pairs in the config file

        """
        file_path: Path = self.__workflow_data.get_config_file_from_active_workflow_instance(
            workflow_instance_name, config_file_name)
        return ConfigFile(config_file_name, file_path)

    def create_new_version_of_workflow_instance(
            self, workflow_instance_name: str, changed_files: List[ReducedConfigFile], version_note: str):
        """Causes the creation of a new version of the workflow instance in the database.

        The new version is obtained by overwriting the given changed files and adopting all other files of the
        predecessor version. The predecessor of the new version is the active version of the instance.

        Args:
            workflow_instance_name (str): The identifier of the workflow instance of which a new version is created
            changed_files (Path): The config-files that were changed in comparison to the predecessor version
                in key-value-pair representation
            version_note (str): Note about the new version given by the user

        """
        # first check if the wf instance exists
        if workflow_instance_name not in os.listdir(self.__versions_base_directory):
            raise InternalException("Internal Error: " + workflow_instance_name + " doesn't refer to a wf instance.")

        # request current version from database
        current_version_number: VersionNumber = \
            VersionNumber(self.__workflow_data.get_active_version_of_workflow_instance(workflow_instance_name))

        # calculate the new version number from the current one
        existing_version_numbers: List[str] = self.__workflow_data.get_version_numbers_of_workflow_instance(
            workflow_instance_name)
        new_version_number: VersionNumber = current_version_number.get_successor(existing_version_numbers)

        # create directory for the new version
        workflow_dir: Path = self.__versions_base_directory / workflow_instance_name  # this dir should already exist
        version_dir: Path = workflow_dir / new_version_number.get_number()
        os.makedirs(version_dir)  # create new dir

        # request changed files from the predecessor version
        old_files: List[Path] = []
        for file in changed_files:
            file_name = file.get_file_name()
            file_path = self.__versions_base_directory / workflow_instance_name / "current_conf" / (file_name + ".conf")

        # copy the old files into the new directory
        for file in old_files:
            shutil.copy(file, version_dir)

        # apply all the changes to the files in the new directory
        for update in changed_files:
            file_name: str = update.get_file_name()
            changed_file: ConfigFile = ConfigFile(file_name, version_dir / (file_name + ".conf"))
            changed_file.apply_changes(update)

        # make new files read-only? TODO

        # create new DatabaseVersion object and make createVersion-request in the WorkflowData
        new_version: DatabaseVersion = DatabaseVersion(new_version_number, version_note, version_dir)
        self.__workflow_data.create_new_version_of_workflow_instance(
            workflow_instance_name, new_version, current_version_number.get_number())

    def get_versions_from_workflow_instance(self, workflow_instance_name: str) -> List[FrontendVersion]:
        """Returns a detailed overview of all versions of the given workflow instance.

                Requests information about all the versions of the given workflow instance from the database.
                Afterwards calculates the difference to the predecessor for every version and returns that information
                in combination with the version numbers and version notes.

                Args:
                    workflow_instance_name (str): The identifier of the workflow instance

                Returns:
                    List[FrontendVersion]: The list version objects that contain the required information

                """
        # request to database to get a DatabaseVersion object for every version
        versions: List[DatabaseVersion] = \
            self.__workflow_data.get_database_versions_of_workflow_instance(workflow_instance_name)

        # create result buffer
        frontend_versions: List[FrontendVersion] = []

        # iterate through all versions
        for version in versions:
            # find out the predecessor version
            if version.get_version_number().get_number() != "1":
                predecessor_number: VersionNumber = version.get_version_number().get_predecessor()
                changed_dir: Path = version.get_changed_config_files()
                file_names: List[str] = os.listdir(changed_dir)

                # get the unchanged file for all changed files
                comparison_files: List[Tuple[str, Path]] = []
                for file_name in file_names:
                    file_path: Path = self.__workflow_data.get_config_file_from_workflow_instance(
                        workflow_instance_name, file_name, predecessor_number.get_number())
                    comparison_files.append((file_name, file_path))

                # calculate the FrontendVersion and put it into the result list
                frontend_versions.append(version.get_frontend_version(comparison_files))

        # return result
        return frontend_versions

    def set_active_version_through_number(self, workflow_instance_name: str, version_number: str):
        """Changes the active version of a workflow instance in the database.

        Before requesting the change in the database a call to the airflow api is made to make sure the workflow
        instance isn't currently running.

        Args:
            workflow_instance_name (str): The name of the workflow instance of which the active version shall be changed
            version_number (str): The number of the new active version

        """
        # first check if the instance is currently running
        dag_request = requests.get(self.__airflow_address + "api/v1/dags/{dag_id}/details")
        # TODO

        # TODO adjust current_conf-dir

        # if not tell database to change the active version
        self.__workflow_data.set_active_version_through_number(workflow_instance_name, version_number)
        pass

    # private methods

    @staticmethod
    def __copy_files_with_extension(src: Path, dst: Path, extension: str):
        # this method shall copy all files under src (we assume the dir is flat) with the given file extension
        # before the call the dst directory itself must not exist
        # if extension == "" files with any extensions are copied

        # create dst directory
        os.mkdir(dst)
        for file in os.listdir(src):
            if extension == "" or os.path.splitext(file)[1] == extension:
                shutil.copy(src / file, dst)
