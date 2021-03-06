import json
from matflow.exceptionpackage.MatFlowException import MatFlowException


class ExceptionHandler:

    """
    This class handles all MatFlowExceptions and those who inherit from MatFlowException.
    It is responsible for preparing the status code for the response.
    """

    @staticmethod
    def handle_exception(exception: MatFlowException) -> str:
        """
        prepares json response when an exception was thrown

        Args:
            exception(MatFlowException): exception that was thrown

        Returns:
            String: status code nested in json object
        """
        return json.dumps(
            ExceptionHandler.send_status_code(
                exception.get_status_code(), {"error_message": exception.message}
            )
        )

    @staticmethod
    def success(out_dict: dict) -> str:
        """
        prepares json response when a request was successful

        Args:
            out_dict(dict): dictionary that needs status code to be added to it

        Returns:
            String: json object containing success status code (607)
        """
        return json.dumps(ExceptionHandler.send_status_code(607, out_dict))

    @staticmethod
    def send_status_code(status_code: int, unfinished_dict: dict) -> dict:
        status_code_dict: dict = {"statusCode": status_code}
        unfinished_dict.update(status_code_dict)
        return unfinished_dict
