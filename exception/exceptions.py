
import sys

class CustomException(Exception):
    """
    Custom exception class for the TradingBot application.
    Captures error message, file name, and line number for easier debugging.
    """

    def __init__(self, error_message: Exception, error_details: sys) -> None:
        """
        Initializes the CustomException.

        Parameters
        ----------
        error_message : Exception
            The original exception/error message.
        error_details : sys
            The sys module, used to extract traceback information.
        """
        self.error_message: Exception = error_message
        _, _, exc_tb = error_details.exc_info()
        self.lineno = exc_tb.tb_lineno if exc_tb else None
        self.file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else None

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the exception.

        Returns
        -------
        str
            The formatted error message with file name and line number.
        """
        return (
            f"Error occurred in python script name [{self.file_name}] "
            f"line number [{self.lineno}] error message [{self.error_message}]"
        )


# if __name__ == '__main__':
#     try:
#         a = 1 / 0
#         print("This will not be printed", a)
#     except Exception as e:
#         raise CustomException(e, sys)
