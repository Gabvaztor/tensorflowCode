import sys, os
from src.utils.Prints import pt

class Logger:

    def write_log_error(self, err):

        exc_type, exc_obj, exc_tb = sys.exc_info()  # this is to get error line number and description.
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]  # to get File Name.
        error_string = "ERROR : Error Msg:{},File Name : {}, Line no : {}\n".format(err, file_name,
                                                                                    exc_tb.tb_lineno)
        pt(error_string)
        file_log = open("python_prediction_error_log.log", "a")
        file_log.write(error_string + "\n\n" + str(err))
        file_log.close()