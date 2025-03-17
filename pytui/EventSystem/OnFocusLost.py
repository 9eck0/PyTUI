from EventSystem.Event import *
from typing import Callable, Any


class OnFocusLostEventArgs(EventArgs):

    def __init__(self, **kwargs):
        EventArgs.__init__(self, **kwargs)


class OnFocusLostEvent(Event):

    def __init__(self, *subscribers: Callable[[Any, OnFocusLostEventArgs], None]):
        Event.__init__(self, *subscribers)

    def invoke(self, sender):
        """
        Notifies all subscribers about the object losing focus.

        Args:
            sender:
        """

        Event.invoke(self, sender, OnFocusLostEventArgs())
