import json
from Implementierung.ExceptionPackage.matflowexception import MatFlowException


class ExceptionHandler:

    """
    This class handles all MatFlowExceptions and those who inherit from MatFlowException.
    It is responsible for preparing the status code for the response.
    """
    def handle_exception(self, exception: MatFlowException) -> str:
        """
        prepares json response when an exception was thrown

        Args:
            exception(MatFlowException): exception that was thrown

        Returns:
            String: status code nested in json object
        """
        return json.dumps(self.__send_status_code(exception.get_status_code(), dict()))

    def success(self, out_dict: dict) -> str:
        """
        prepares json response when a request was successful

        Args:
            out_dict(dict): dictionary that needs status code to be added to it

        Returns:
            String: json object containing success status code (607)
        """
        return json.dumps(self.__send_status_code(607, out_dict))

    @staticmethod
    def __send_status_code(status_code: int, unfinished_dict: dict) -> dict:
        status_code_dict: dict = {'status_code': status_code}
        unfinished_dict.update(status_code_dict)
        return unfinished_dict
