"""
The central adapter interface for interactivity with terminal systems.

Due to the differing capabilities of each terminal system, manu commands herein are controlled by a capability check
during PyTUI's initialization step.
"""

import atexit       # Restore initial terminal state on program exit
import os
import shutil
import sys
from enum import StrEnum
from typing import Callable

_NT_SYSTEM = "nt"
_UNIX_SYSTEM = "posix"

if os.name == _UNIX_SYSTEM:
    import termios
    import tty


#region ================ TerminalFunction class ================

class TerminalFunction:
    """
    Declares a platform-agnostic, capability-aware, callable terminal function.

    During instancing, one or more main function calls must be provided, depending on the required platform support of
    the terminal.

    An optional capability support testing function should also be provided, on the basis that the
    specified functionality's support by the terminal can be programmatically tested (e.g. ANSI escape support).
    If attempting to call this function when the capability test has failed, a NotImplementedError will be thrown,
    unless suppressed using silence_unsupported_errors flag.
    """

    def __init__(self,
                 name: str,
                 func: Callable,
                 func_nt: Callable = None,
                 capability_test: Callable[[], bool] | True = True):
        """
        Creates a platform-agnostic terminal function call.

        :param name: the readable name of the capability.
        :param func: the Unix-specific terminal function call; if func_nt is not specified,
                     this function defaults as the platform-agnostic implementation.
        :param func_nt: the Windows-specific terminal function call.
        :param capability_test: a function to test terminal capability support; must output a boolean.
        """

        self.name = name

        # Perform terminal support
        self.test = capability_test
        self.supported = capability_test()
        if not isinstance(self.supported, bool):
            raise TypeError("capability_test() requires a boolean output, obtained instead: " + type(self.supported))

        self._posix_call = func
        self._nt_call = func_nt

        self.silence_unsupported_errors = False
        """ Whether compatibility errors are suppressed when attempting to call the function. """

    def __call__(self, *args, **kwargs):
        if not self.supported and not self.silence_unsupported_errors:
            raise NotImplementedError(f"{self.name} is not supported by the current terminal system.")

        try:
            if self._nt_call is not None and os.name == _NT_SYSTEM:
                return self._nt_call(*args, **kwargs)
            else:
                return self._posix_call(*args, **kwargs)
        except TypeError as e:
            # Reframe function call error messages to usefully describe with current terminal function name
            new_msg = e.args[0]
            new_msg = new_msg[new_msg.find("()") + 2:]
            new_msg = f"Calling '{self.name}'{new_msg}"
            e.args = (new_msg, *e.args[1:])
            raise e

    def call(self, *args, **kwargs):
        return self(*args, **kwargs)

#endregion TerminalFunction class


#region ================ ANSI escape sequences ================

class EscapeSequences(StrEnum):
    """
    Collection of ANSI escape sequences (ISO/IEC 6429) supported by PyTUI.

    All ANSI escape sequences are escaped with the leading escape character (ESC): '\x1b' == '\033'.

    The vast majority of escape sequences within this Enum are part of the Fe escape sequence type.
    Their operability are subject to the terminal system's support of ISO/IEC 2022, particularly
    their conformance of the C1 control codes group.
    """

    # Fe commands set

    CLEAR_SCREEN = "\033[2J"
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    ERASE_LINE = "\033[K"

#endregion


_original_terminal_state = None
if os.name == _UNIX_SYSTEM:
    _original_terminal_state = termios.tcgetattr(sys.stdin)


def _func_erase_terminal():
    # Two versions: 1) system call interfacing with terminal; 2) create new alternate screen buffer
    os.system("clear")
    print("\x1b[?1049h")
erase_terminal = TerminalFunction(
    name="erase_terminal",
    func=_func_erase_terminal,
    func_nt=lambda: {
        os.system("cls")
    },
    capability_test=lambda: {

    }
)


def func_enable_alt_screenbuffer():
    print("\x1b[?1049h")
    erase_terminal()
enable_alternate_screen_buffer = TerminalFunction(
    name="enable_alternate_screen_buffer",
    func=func_enable_alt_screenbuffer,
    capability_test=lambda: {

    }
)


def func_disable_alt_screenbuffer():
    print("\x1b[?1049l")
disable_alternate_screen_buffer = TerminalFunction(
    name="disable_alternate_screen_buffer",
    func=func_disable_alt_screenbuffer,
    capability_test=lambda: {

    }
)


#endregion


def get_terminal_size():
    return shutil.get_terminal_size()


def _on_exit():
    if os.name == _UNIX_SYSTEM:
        # Revert to initial terminal state
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, _original_terminal_state)
    pass

atexit.register(_on_exit)
