"""
Base class to all view components.

This module defines the Component class, a required inheritance for custom
view components in order to be properly supported by the ShellGUI system.

When implementing a custom component, for each overloaded method, the base method
must be called upon by substituting the 'self' parameter as that of the custom
component.

The event system in components is comprised of two action points:
1) The implementer creates event handlers for their custom components
2) The ShellGUI registers event handlers per event type

Additional interactivity can be supported on custom Components by inheriting from UI.ABC
explicitly. Note that all implemented ABCs must be declared after the Component base class
in the class declaration. Care must be taken to ensure compliance with Python's method
resolution order (MRO).
TODO
"""

from pytui.EventSystem.OnFocusLost import OnFocusLostEvent
from pytui.EventSystem.KeyPress import KeyPressEvent
from pytui.EventSystem.OnFocus import OnFocusEvent
from pytui.UI.ABC.BaseComponent import BaseComponent
from pytui.UI.ABC.Focusable import Focusable



class Component(BaseComponent, Focusable):

    #====================Magic methods====================

    def __init__(self, width: int, height: int, location: (int, int) = None):

        super().__init__(width=width, height=height, location=location)

        # ======== Internal Properties ========

        # ======== Layout Properties ========

        # ======== Appearance Properties ========

        # ======== Behavior Properties ========

        self._focused = False
        """ The focus state of this component. """

        self.handledInput = False
        """ Determines whether the GUI should transmit input to the component. """

        # ======== Event system registration ========

        self._on_focus = OnFocusEvent()
        self._on_focus_lost = OnFocusLostEvent()
        self._on_key_press = KeyPressEvent()

    def __eq__(self, other):
        return str(self) == str(other)

    def __repr__(self):
        return self.value()

    #====================Methods====================

    def value(self):
        """
        Each component should be a string which, when printed, yields a rectangular footprint.

        Returns:
            A string representing the component.
        """
        return ""

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

    @property
    def OnKeyPress(self):
        return self._on_key_press
    @OnKeyPress.setter
    def OnKeyPress(self, value):
        if value is not self._on_key_press:
            # Trying to set a new event listener object
            if not isinstance(value, KeyPressEvent):
                raise TypeError(f"Attempting to set an incompatible object as an OnKeyPress event listener: {type(value)}")
            self._on_key_press = value

    #====================Properties====================

    @property
    def focused(self):
        """
        Whether the component is receiving focus.
        """
        return self._focused
    @focused.setter
    def focused(self, value: bool):
        """
        Notifies this component's OnFocus event listener when it receives focus.
        Notifies this component's FocusLost event listener when focus is lost.
        """
        if value:
            self._focused = True
            self.OnFocus.invoke(sender=self)
        else:
            self._focused = False
            self.OnFocusLost.invoke(sender=self)

    @property
    def height(self):
        """
        Returns the width, in characters, of the UI.

        Returns:
            an integer representing the height of the UI
        """
        return self._height
    @height.setter
    def height(self, value: int):
        """
        Specifies the height, in characters, of the UI.

        Args:
            value: an integer specifying the height of the UI
        """
        self._height = int(value)

    @property
    def location(self):
        """
        The location of the component inside the UI.

        Returns:
            a tuple specifying the component's (x, y) location inside the UI
        """
        return self._location
    @location.setter
    def location(self, value):
        """
        Sets the location of the component inside the UI.

        Args:
            value: a tuple specifying the component's (x, y) location inside the UI
        """
        self._location = (value[0], value[1])

    @property
    def width(self):
        """
        Returns the width, in characters, of the UI.

        Returns:
            an integer representing the width of the UI
        """
        return self._width
    @width.setter
    def width(self, value: int):
        """
        Specifies the width, in characters, of the UI.
        Set to 0 for

        Args:
            value: an integer specifying the width of the UI
        """
        self._width = int(value)
