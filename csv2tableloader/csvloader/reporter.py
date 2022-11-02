
import sys
import os
from enum import Enum

class TextStyle:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Reporter:
    _log_file = None

    @staticmethod
    def init():
        os.system('')

        Reporter._log_file = open('game_data_verify.log', 'w', encoding='utf-8')

    @staticmethod
    def close():
        if None != Reporter._log_file:
            Reporter._log_file.close()
            Reporter._log_file = None

    @staticmethod
    def info(message):
        print(TextStyle.WHITE + TextStyle.BOLD + message + TextStyle.WHITE)

        Reporter._log_file.write(f'info - {message} \n')

    @staticmethod
    def warning(message):
        print(TextStyle.YELLOW, message, TextStyle.WHITE)

        Reporter._log_file.write(f'warning - {message} \n')

    @staticmethod
    def error(message):
        print(TextStyle.RED, message, TextStyle.WHITE)

        Reporter._log_file.write(f'error - {message} \n')

    @staticmethod
    def fatal(message):
        print(TextStyle.PURPLE, TextStyle.BOLD, message, TextStyle.WHITE)

        Reporter._log_file.write(f'fatal - {message} \n')
        #sys.exit(-1)
