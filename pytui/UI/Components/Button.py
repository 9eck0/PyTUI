"""
This module defines the Button view component.
"""


from UI.Appearance import BorderTypes
from Label import Label
from EventSystem.KeyPress import KeyPressEventHandler, KeyPressEventArgs
from EventSystem.KeyCodes import KeyCodes
from typing import Callable


# ======================== Common Functions ========================

# no function


#region ======================== Button ========================

class Button(Label):

    def __init__(self, location, text: str, action: Callable[[], None] = None,
                 bordertype=BorderTypes.ThinBorder,
                 length=-1, overflowindicator="…"):
        # Base initialization
        Label.__init__(self, location=location, text=text,
                       showborder=True, bordertype=bordertype,
                       length=length, overflowindicator=overflowindicator)
        # Event handler
        self.OnKeyPress += self._onKeyPress
        self.OnKeyPress += action
        self.Action = action

    def _onKeyPress(self, sender, args: KeyPressEventArgs):
        if self.Action is not None and args.Key in (KeyCodes.Enter, KeyCodes.Return):
            self.Action()

#endregion Button

#region ======================== Version History ========================

# 1.0
"""
    Refactored Button class out of ShellGUI_Forms.py.

    Additions
    ---------
        -Button(Label) class
            -A button is a focusable and clickable label.
"""

#endregion Version History
