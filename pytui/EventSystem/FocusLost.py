"""
.NET-style event system in Python
The aim of this module is to create an event system using only Python's base installation (e.g. no Anaconda, PyPy, etc.)
"""

if __name__ == "__main__":
    # MAJOR +1 represents an added function.
    __MAJOR = 1
    # MINOR +1 represents a change in existing function(s) within the current MAJOR.
    __MINOR = 0

    __info = """This file contains the module 'FocusLost', used to integrate ShellGUI component losing focus events.
To use this module in another project, include this file inside the project's directory."""

    print("========================================================")
    print("FocusLost.py version ", __MAJOR, ".", __MINOR, sep='', end='\n\n')
    print(__info)
    print("========================================================\n")
    input("Press enter to continue...")


#region ======================== Imports ========================

# Used by:

from EventSystem.Event import *
from typing import Callable, Any

#endregion Imports


# ======================== Common Functions ========================

# no function


#region ======================== FocusLostEventArgs ========================

class FocusLostEventArgs(EventArgs):

    def __init__(self, **kwargs):
        EventArgs.__init__(self, **kwargs)

#endregion FocusLostEventArgs


#region ======================== FocusLostEventListener ========================

class FocusLostEventListener(EventListener):

    def __init__(self, *subscribers: Callable[[Any, FocusLostEventArgs], None]):
        EventListener.__init__(self, *subscribers)

    def notify(self, sender):
        """
        Notifies all subscribers about the object gaining focus.

        Args:
            sender:
        """

        EventListener.notify(self, sender, FocusLostEventArgs())

#endregion FocusLostEventListener


#region ======================== FocusLostEventHandler ========================

class FocusLostEventHandler(EventHandler):

    def __init__(self, *subscribers: Callable[[Any, FocusLostEventArgs], None]):

        EventHandler.__init__(self, FocusLostEventListener(*subscribers))

#endregion FocusLostEventHandler


#region ======================== Version History ========================

# 1.0
"""
    Initial Release
    Event system for detecting when a ShellGUI component lost focus.

    Additions
    ---------
        -class KeyPressEventArgs implements EventArgs
            -__init__(self, key, **kwargs)
        -class _KeyPressEventListener implements EventListener
            -__init__(self, *subscribers)
            -notify(self, sender, key)
        -class KeyPressEventHandler implements EventHandler
            -__init__(self, *subscribers)
            -readkey(self)
            -class UnixKeyPress
                -__init__(self)
                -__call__(self)
            -class WindowsKeyPress
                -__init__(self)
                -__call__(self)
        -class KeyCodes
            -Defined constants (under this class) for all latin1 unicode characters
            -CombinationCharacters dictionary for special keyboard functions that cannot be represented as a single
             Unicode character
            -static tostring(key1: bytes, key2: bytes)
"""

#endregion Version History
