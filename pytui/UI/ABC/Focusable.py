"""
Implement this abstract base class to define focusable UI components.

Hooks in the background to the unified FocusManager
"""

from abc import ABC, abstractmethod
from enum import Enum

from Color import ColorHandler
from pytui.EventSystem.OnFocus import OnFocusEvent
from pytui.EventSystem.OnFocusLost import OnFocusLostEvent


class FocusFeedback(Enum):
    NONE = 0,
    HALO = 1,
    FLASH = 2


class Focusable(ABC):
    """
    Feature extension for components, allowing focus to be caught by the implementing component.

    Gaining focus is the first step in interacting with a component. Hence, this class is a mandatory implementation
    for other extensions
    """

    def __init__(self):

        self._focusable = True
        """ Whether this component can receive focus. """

        self._focused = False
        """ The focus state of this component. """

        self.focus_index = 0
        """
        Indicates the ascending order in which this component should receive focus within the parent container.
        
        If multiple components have the same index, the order is determined by layout from left to right,
        then from top to bottom.
        """

        self._focus_feedback_mode: FocusFeedback = FocusFeedback.FLASH
        """ Visual indicator for focus locking  """

        self._highlight_fill: int | ColorHandler | None = None
        """ The highlight color for when this component is focused. Set to None for default terminal text color. """

        self._highlight_border_color: int | ColorHandler | None = None
        """ Color of the border when this component is focused. Set to None to be determined automatically by
            the highlight fill color. """

        # Event system registration

        self._on_focus = OnFocusEvent()
        self._on_focus_lost = OnFocusLostEvent()

    #==================== Properties =====================

    @property
    def focusable(self):
        """
        Whether this component can receive focus.

        While this is an independent property value, a component's Enabled property will override the focusable behavior
        as False by the TUI.

        If this is set as False on a container, its children are still focusable unless the container itself is
        set as disabled.
        """
        return self._focusable
    @focusable.setter
    def focusable(self, value):
        """
        Sets whether this component can receive focus.

        While this is an independent property value, a component's Enabled property will override the focusable behavior
        as False by the TUI.

        If this is set as False on a container, its children are still focusable unless the container itself is
        set as disabled.
        """
        self._focusable = value
        if value is False and self.focused:
            # Unfocus and shift to next focus
            self.focused = False

    @property
    def focused(self):
        """
        Whether this component is receiving focus.
        """
        return self._focused
    @focused.setter
    def focused(self, value: bool):
        """
        Sets the focus state of this component.

        When it receives focus, notifies this component's OnFocus event listener.

        When focus is lost, notifies this component's FocusLost event listener, and sets focus to its parent.
        """
        if value and self._focused is False:
            self._focused = True
            self.OnFocus.invoke(sender=self)
        elif value is False and self._focused:
            self._focused = False
            self.OnFocusLost.invoke(sender=self)

    @property
    def focus_feedback_mode(self):
        return self._focus_feedback_mode
    @focus_feedback_mode.setter
    def focus_feedback_mode(self, value: FocusFeedback | int):
        if value not in FocusFeedback._value2member_map_:
            raise ValueError("Invalid focus feedback mode specified")
        self._focus_feedback_mode = value

    @property
    def highlight_fill(self):
        return self._highlight_fill
    @highlight_fill.setter
    def highlight_fill(self, value: int | ColorHandler | None):
        if isinstance(value, int):
            value = ColorHandler(value)
        self._highlight_fill = value

    @property
    def highlight_border_color(self):
        if self._highlight_border_color is not None:
            return self._highlight_border_color
        else:
            # Returns a slight contrasting shade of the highlight fill color
            return self.highlight_fill
    @highlight_border_color.setter
    def highlight_border_color(self, value: int | ColorHandler | None):
        if isinstance(value, int):
            value = ColorHandler(value)
        self._highlight_border_color = value
    
    #==================== Event Listeners =====================

    @property
    def OnFocus(self):
        return self._on_focus
    @OnFocus.setter
    def OnFocus(self, value):
        if value is not self._on_focus:
            # Trying to set a new event listener object
            if not isinstance(value, OnFocusEvent):
                raise TypeError(f"Attempting to set an incompatible object as an OnFocus event listener: {type(value)}")
            self._on_focus = value
        # else: no need to perform setter operation on the same object, e.g. OnFocus += method

    @property
    def OnFocusLost(self):
        return self._on_focus_lost
    @OnFocusLost.setter
    def OnFocusLost(self, value):
        if value is not self._on_focus_lost:
            # Trying to set a new event listener object
            if not isinstance(value, OnFocusLostEvent):
                raise TypeError(f"Attempting to set an incompatible object as an OnFocusLost event listener: {type(value)}")
            self._on_focus_lost = value
