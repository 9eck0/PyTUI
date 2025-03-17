"""
.NET-style event system in Python
The aim of this module is to create an event system using only Python's base installation (e.g. no Anaconda, PyPy, etc.)
"""

from EventSystem.Event import *
from typing import Callable, Any



#======================== Common Functions ========================

# no function


#region ======================== OnFocusEventArgs ========================

class OnFocusEventArgs(EventArgs):

    def __init__(self, **kwargs):
        EventArgs.__init__(self, **kwargs)

#endregion OnFocusEventArgs


#region ======================== OnFocusEventListener ========================

class OnFocusEvent(Event):

    def __init__(self, *subscribers: Callable[[Any, OnFocusEventArgs], None]):
        Event.__init__(self, *subscribers)

    def invoke(self, sender):
        """
        Notifies all subscribers about the object gaining focus.

        Args:
            sender:
        """

        Event.invoke(self, sender, OnFocusEventArgs())

#endregion OnFocusEventListener
