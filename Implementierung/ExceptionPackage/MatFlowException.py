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
        return self.status_code


class UserExistsException(MatFlowException):

    """
    This is an exception that is thrown when a user does not exist.
    """

    def __init__(self, message: str):
        """
        constructs a new UserExistsException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        self.__status_code = 601
        super(UserExistsException, self).__init__(message, self.__status_code)


class DoubleTemplateNameException(MatFlowException):

    """
    This is an exception that is thrown when the desired template name already exists.
    """

    def __init__(self, message: str):
        """
        constructs a new DoubleTemplateNameException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        self.__status_code = 602
        super(DoubleTemplateNameException, self).__init__(message, self.__status_code)


class InvalidDagFileException(MatFlowException):

    """
    This is an exception that is thrown when the dag definition file is not correct (when dag file is finished coding).
    """

    def __init__(self, message: str):
        """
        constructs a new InvalidDagFileException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        self.__status_code = 603
        super(InvalidDagFileException, self).__init__(message, self.__status_code)


class DoubleWorkflowInstanceNameException(MatFlowException):

    """
    This is an exception that is thrown when the desired workflow instance name already exists.
    """

    def __init__(self, message: str):
        """
        constructs a new DoubleWorkflowInstanceNameException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        self.__status_code = 604
        super(DoubleWorkflowInstanceNameException, self).__init__(
            message, self.__status_code
        )


class EmptyConfigFolderException(MatFlowException):

    """
    This is an exception that is thrown when the config folder is empty, meaning that no config can be selected.
    """

    def __init__(self, message: str):
        """
        constructs a new EmptyConfigFolderException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        self.__status_code = 605
        super(EmptyConfigFolderException, self).__init__(message, self.__status_code)


class WorkflowInstanceRunningException(MatFlowException):

    """
    This is an exception that is thrown when the workflow instance is already running.
    """

    def __init__(self, message: str):
        """
        constructs a new WorkflowInstanceRunningException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        self.__status_code = 606
        super(WorkflowInstanceRunningException, self).__init__(
            message, self.__status_code
        )


class UnrepresentableDagException(MatFlowException):

    """
    This is an exception that is thrown when the dag cannot be previewed
    (when dag file editing is in progress (JUST preview)).
    """

    def __init__(self, message: str):
        """
        constructs a new UnrepresentableDagException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        self.__status_code = 608
        super(UnrepresentableDagException, self).__init__(message, self.__status_code)


class LoginException(MatFlowException):

    """
    This is an exception that is thrown when the login failed.
    """

    def __init__(self, message: str):
        """
        constructs a new LoginException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        self.__status_code = 609
        super(LoginException, self).__init__(message, self.__status_code)


class SignUpException(MatFlowException):

    """
    This is an exception that is thrown when the sign up failed.
    """

    def __init__(self, message: str):
        """
        constructs a new LoginException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        self.__status_code = 610
        super(SignUpException, self).__init__(message, self.__status_code)


class ConverterException(MatFlowException):

    """
    This is an exception that is thrown when the conversion failed.
    """

    def __init__(self, message: str):
        """
        constructs a new ConverterException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        self.__status_code = 611
        super(ConverterException, self).__init__(message, self.__status_code)


class AirflowConnectionException(MatFlowException):
    """
    Exception when airflow container has not been started yet.
    """
    def __init__(self, message: str):
        """
        constructs new AirflowConncetionException

        Args:
            message: The message that is displayed when this exception is thrown.
        """
        self.__status_code = 612
        super(AirflowConnectionException, self).__init__(message, self.__status_code)



class InternalException(MatFlowException):
    """
    Exception for dev purposes
    """

    def __init__(self, message: str):
        self.__status_code = 666
        super(InternalException, self).__init__(message, self.__status_code)
