class MatFlowException(Exception):
    """
    This is the MatFlow parent exception from which all the specified exceptions inherit.
    It adds more functionality to a standard exception through the exception’s status code
    and function which gets the status code. This is important for our API Package.
    """
    def __init__(self, message: str, status_code: int):
        """
        constructs a new MatFlowException

        Args:
            message: The message shown when exception is raised
            status_code: the exception's status code
        """
        self.message = message
        self.status_code = status_code
        super(MatFlowException, self).__init__(message)

    def get_status_code(self) -> int:
        """
        gets the status code

        Returns:
             int: the status code
        """

class UserExistsException(MatFlowException):

    """
    This is an exception that is thrown when a user does not exist.
    """

    __status_code: int = 601


    def __init__(self, message: str):
        """
        constructs a new UserExistsException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        super(UserExistsException, self).__init__(message, __status_code)


class DoubleTemplateNameException(MatFlowException):

    """
    This is an exception that is thrown when the desired template name already exists.
    """

    __status_code: int = 602


    def __init__(self, message: str):
        """
        constructs a new DoubleTemplateNameException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        super(DoubleTemplateNameException, self).__init__(message, __status_code)


class InvalidDagFileException(MatFlowException):

    """
    This is an exception that is thrown when the dag definition file is not correct (when dag file is finished coding).
    """

    __status_code: int = 603


    def __init__(self, message: str):
        """
        constructs a new InvalidDagFileException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        super(InvalidDagFileException, self).__init__(message, __status_code)

class DoubleWorkflowInstanceNameException(MatFlowException):

    """
    This is an exception that is thrown when the desired workflow instance name already exists.
    """

    __status_code: int = 604


    def __init__(self, message: str):
        """
        constructs a new DoubleWorkflowInstanceNameException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        super(DoubleWorkflowInstanceNameException, self).__init__(message, __status_code)


class EmptyConfigFolderException(MatFlowException):

    """
    This is an exception that is thrown when the config folder is empty, meaning that no config can be selected.
    """

    __status_code: int = 605


    def __init__(self, message: str):
        """
        constructs a new EmptyConfigFolderException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        super(EmptyConfigFolderException, self).__init__(message, __status_code)


class WorkflowInstanceRunningException(MatFlowException):

    """
    This is an exception that is thrown when the workflow instance is already running.
    """

    __status_code: int = 606


    def __init__(self, message: str):
        """
        constructs a new WorkflowInstanceRunningException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        super(WorkflowInstanceRunningException, self).__init__(message, __status_code)


class UnrepresentableDagException(MatFlowException):

    """
    This is an exception that is thrown when the dag cannot be previewed
    (when dag file editing is in progress (JUST preview)).
    """

    __status_code: int = 608


    def __init__(self, message: str):
        """
        constructs a new UnrepresentableDagException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        super(UnrepresentableDagException, self).__init__(message, __status_code)


