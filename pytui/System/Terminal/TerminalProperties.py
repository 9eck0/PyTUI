"""
This file contains utility functions to interface with the native terminal host.
"""
import os
import sys
from enum import Enum


class TerminalCapabilities:
    def __init__(self, name: str):
        self.name = name
        """ The fully-qualified readable name of the terminal application. """

        self.color_support = 0
        """ The color capability of the terminal """


class TerminalTypes(Enum):
    Printer = 0
    """ Unknown terminal type with minimal supported capabilities. """
    Bash = 1
    ConsoleHost = 2
    Idle = 3


# TODO: function to obtain terminal host name/type  (e.g. IDLE, bash, cmd)
def identify_terminal():
    match sys.platform:
        case "win32":
            pass
        case "posix":
            pass
        case "java":
            pass
        case _:
            raise NotImplementedError("This operating system is incompatible with ")


# TODO: function to evaluate terminal window width


reset_text_colors_code = "\033[39;49m"

reset_text_attributes_code = "\033[0m"
