"""
This file contains the concrete global implementation of PyTUI's keyboard listener.

Once initialized, it runs in the background until manual stopping or Python
program exit, and catches all keyboard presses to output as Unicode character
sequences.
"""

import os
from pytui.EventSystem.Event import Event
from pytui.EventSystem.KeyPress import KeyPressEventArgs
from pytui.EventSystem.KeyCodes import KeyCodes


class __UnixKeyPress:
    """
    Credits:
        https://code.activestate.com/recipes/134892/
    """

    def __init__(self):
        import sys, tty, termios

    def __call__(self):
        import sys, tty, termios
        try:
            stdin_file = sys.stdin.fileno()
            tty_attr = termios.tcgetattr(stdin_file)

            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(stdin_file, termios.TCSADRAIN, tty_attr)

        return ch


class __WindowsKeyPress:
    """
    Credits:
        https://code.activestate.com/recipes/134892/
    """

    def __init__(self):
        try:
            import msvcrt
        except ImportError as e:
            e.msg = (f"An error occurred while importing module '{e.name} ' for KeyPressEventHandler initialization."
                     f"Does this system lack the required module?")
            raise e

    def __call__(self):
        try:
            import msvcrt
            return msvcrt.getch()
        except ImportError as e:
            e.msg = (f"An error occurred while importing module '{e.name} ' for KeyPressEventHandler initialization."
                     f"Does this system lack the required module?")
            raise e


if __name__ == "__main__":
    exit()


read_key = __WindowsKeyPress() if os.name == "nt" else __UnixKeyPress()
dispatcher = Event()

def subscribe(handler):
    dispatcher.subscribe(handler)

def dispatch(key1, key2=KeyCodes.Null):
    dispatcher.invoke(None, KeyPressEventArgs(key1, key2))

def read_dispatch():
    """
    Reads the next keypress event and returns a set of two bytecodes.

    This function call is platform-agnostic.
    """

    if os.name == "nt":
        # _getch() in Windows returns a set of two user inputs in latin1 encoding
        keycodes = []
        # We need to call _getch() 3 times per user key input in order to catch combination keys (e.g. Delete key).
        for i in range(2):
            keycodes.append(read_key())
            if keycodes[0] != KeyCodes.Null and keycodes[0] != KeyCodes.FunctionPrefix:
                # If the first key code is not a prefix to a combination key, it is a normal ASCII character.
                # In this instance, default the second key code to null and do not detect key input anymore.
                keycodes.insert(1, KeyCodes.Null)
                break
            i += 1

        dispatcher.invoke(None, keycodes[0], keycodes[1])
    else:
        keycode = read_key()
        dispatcher.invoke(None, keycode[0], keycode[1])

