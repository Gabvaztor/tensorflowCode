import os

CURRENT_DIR = os.path.dirname(__file__)
LOGS_DIR = CURRENT_DIR + r"\logs"
LOGGER_SERVER_PATH = LOGS_DIR + r"\server.log"
ERROR_LOGGER_SERVER_PATH = LOGS_DIR + r"\server_error.log"
LOGGER_CLIENT_PATH = LOGS_DIR + r"\client.log"
ERROR_LOGGER_CLIENT_PATH = LOGS_DIR + r"\client_error.log"

HEADER_LENGTH = 1024
SERVER_PORT = 5056
#HOST_SERVER = "127.0.0.1"
HOST_SERVER = "192.168.1.37"
PUBLIC_IP = ""
#PUBLIC_IP = ""
PUBLIC_IP_ = ""