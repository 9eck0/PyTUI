"""
Implement this abstract base class to define UI components able to receive a click event (Enter/Return key).

This ABC requires and implements the Focusable ABC by default.
"""

from abc import ABC

from EventSystem.OnClick import OnClickEvent, OnClickEventArgs
from UI.ABC.Focusable import Focusable


class Clickable(ABC, Focusable):
    """
    (This ABC implements the Focusable ABC, no need to implement it separately.)

    Extension to components allowing click events to be captured.

    A click is registered when the user presses on the Enter key, the Return key, or the

    Unlike the KeyPressReceiver extension, this feature extension's scope of action can be extended to integrate with
    mouse and touch inputs. It is advisable to not implement both these feature extensions together, as
    """

    def __init__(self):
        super(Focusable).__init__()
