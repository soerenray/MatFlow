
class ExceptionHandler():

    """
    This class handles all MatFlowExceptions and those who inherit from MatFlowException.
    It is responsible for preparing the status code for the response.
    """
    def _handle_exception(self, exception: MatFlowException) -> str:
        """
        prepares json response when an exception was thrown

        Args:
            exception(MatFlowException): exception that was thrown

        Returns:
            String: status code nested in json object
        """
        pass

    def _success(self) -> str:
        """
        prepares json response when a request was successful

        Returns:
            String: json object containing success status code (607)
        """
        pass

    def __send_status_code(self, status_code: int):
        pass