"""
This module defines the OnClick event.

The OnClick event is fired when a click-accepting component receives a valid 'click'.
"""

from EventSystem.Event import *

from enum import StrEnum
from typing import Callable, Any


#======================== Common Functions ========================

# no function


#region ======================== OnClickEventArgs ========================

class ClickType(StrEnum):
    ENTER_KEY = "EnterKey"
    """ Default. OnClick event triggered by the user pressing on the Enter or Return key. """

    RETURN_KEY = "ReturnKey"
    """
    OnClick event triggered by the user pressing on the Return key (Ctrl/Command + Enter).
    Handle only when a distinction is needed between Enter and Return keys.
    """

    LEFT_MOUSE_BUTTON = "LeftMouseButton"
    """ OnClick event triggered by the user interacting with  """

    @classmethod
    def has_value(cls, value):
        return str(value) in cls._value2member_map_


class OnClickEventArgs(EventArgs):

    def __init__(self, click_type: ClickType | str, **kwargs):
        EventArgs.__init__(self, **kwargs)
        self.click_type = click_type

#endregion OnClickEventArgs


#region ======================== OnClickEventListener ========================

class OnClickEvent(Event):

    def __init__(self, *subscribers: Callable[[Any, OnClickEventArgs], None]):
        Event.__init__(self, *subscribers)
        # Subscribe current keypress listener to

    def invoke(self, sender, args: OnClickEventArgs | ClickType):
        """
        Notifies all subscribers about the component gaining focus.

        :param sender:
        :param args:
        """
        if isinstance(args, str):
            if args not in ClickType:
                args = OnClickEventArgs(ClickType.ENTER_KEY)
            else:
                args = OnClickEventArgs(args)
        Event.invoke(self, sender, args)

#endregion OnClickEventListener
