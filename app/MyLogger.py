import logging
import os
import psutil

logging.basicConfig(
    filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)


class MyLogger:
    @staticmethod
    def log_error(_sys, _exception, _message=None):
        if _sys is not None:
            exception_type, exception_object, exception_traceback = _sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            logging.error("Error in file: " + os.path.basename(filename))
            logging.error("Error in line: " + str(line_number))
        logging.error("Error in exception: " + str(_exception))
        if _message is not None:
            logging.error("_message: " + str(_message))

    @staticmethod
    def log_info(_message):
        logging.info(_message)

    @staticmethod
    def log_warning(_message):
        logging.warning(_message)

    @staticmethod
    def log_debug(_message):
        logging.debug(_message)

    @staticmethod
    def print_memory_footprint(tag=None):
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        if tag:
            print("TAG: ", tag)
        print(mem_info.rss)
