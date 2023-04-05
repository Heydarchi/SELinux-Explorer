import logging
import os

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class MyLogger:

    @staticmethod
    def logError(_sys, _exception, _message = None):
        exception_type, exception_object, exception_traceback = _sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        logging.error("Error in file: " + str(filename))
        logging.error("Error in line: " + str(line_number))
        logging.error("Error in exception: " + str(_exception))
        if _message != None:
            logging.error("_message: " + str(_message))
        #logging.error("exception type: ", str(exception_type)+", exception object: " + str(exception_object) + ", exception traceback: " + str(exception_traceback))

    @staticmethod
    def logInfo(_message):
        logging.info(_message)

    @staticmethod
    def logWarning(_message):
        logging.warning(_message)

    @staticmethod
    def logDebug(_message):
        logging.debug(_message)

