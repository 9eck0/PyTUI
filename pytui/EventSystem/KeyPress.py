"""
Enables key presses to be captured and transmitted when the implementing component is being focused.
"""

import System.Terminal.KeyboardListener as GlobalKeyListener
from EventSystem.Event import *
from EventSystem.KeyCodes import KeyCodes
from UI.Components.Component import Component
from typing import Callable, Any


#region ======================== KeyPressEventArgs ========================

class KeyPressEventArgs(EventArgs):

    def __init__(self, key, key2=b'\x00', **kwargs):
        EventArgs.__init__(self, **kwargs)

        # TODO: link back to source component to stop handling
        self.Handled = False
        """Sets whether the KeyPress event has already been handled, stopping any further processing."""

        self.Key = key
        self.Key2 = key2
        if key2 == b'\x00':
            self.isSpecialKey = False
        else:
            self.isSpecialKey = True

#endregion KeyPressEventArgs


#region ======================== KeyPressEventListener ========================

class KeyPressEvent(Event):
    """
    An event listener for key presses on the current Component.

    This event is triggered when the current Component receives a key press while it has focus.
    """

    def __init__(self, component: Component, *subscribers: Callable[[Any, KeyPressEventArgs], None]):
        Event.__init__(self, *subscribers)
        self._parent_component = component
        # Subscribe current keypress listener to the global keypress listener
        GlobalKeyListener.subscribe(self._global_listener_handler)
    
    def _global_listener_handler(self, sender, args: KeyPressEventArgs):
        if self._parent_component is not None and self._parent_component.focused:
            Event.invoke(self, self._parent_component, args)

    def invoke(self, sender, key, key2=b'\x00'):
        """
        Notifies all subscribers about a key press.

        :param sender: The parent component that is receiving the key press.
        :param key: The base key code.
        :param key2: Modifier key code, if available. See KeyCodes class for more info.
        """

        Event.invoke(self, sender, KeyPressEventArgs(key, key2))

#endregion KeyPressEventListener


#region ======================== KeyPressEventHandler ========================

class KeyPressEventHandler:#(EventHandler):

    _NT_SYSTEM = "nt"
    _UNIX_SYSTEM = "posix"

    def __init__(self, *subscribers: Callable[[Any, KeyPressEventArgs], None]):

        if os.name == self._NT_SYSTEM:
            self._getch = KeyPressEventHandler.__WindowsKeyPress()
        else:       # fallback method. Most likely os.name == 'posix'
            self._getch = KeyPressEventHandler.__UnixKeyPress()

        #EventHandler.__init__(self, KeyPressEventListener(*subscribers))

    def readKey(self, decode=False):
        """
        Updates methods and functions subscribed to this event handler.

        Any subscriber must implement the exact parameters: subscriber(sender, args: KeyPressEventArgs)
        where parameter 'args' contains the string character mapped from the pressed key.

        :param decode: Whether to decode the immediate key code into the corresponding character.
            Note: this should be left at False if needing to detect special function keys (e.g. ArrowUp).
        """

        if os.name == self._NT_SYSTEM:
            # _getch() in Windows returns a set of two user inputs in latin1 encoding
            keycodes = []
            # We need to call _getch() 3 times per user key input in order to catch combination keys (e.g. Delete key).
            for i in range(2):
                keycodes.append(self._getch())
                if keycodes[0] != KeyCodes.Null and keycodes[0] != KeyCodes.FunctionPrefix:
                    # If the first key code is not a prefix to a combination key, it is a normal ASCII character.
                    # In this instance, default the second jey code to null and do not detect key input anymore.
                    keycodes.insert(1, KeyCodes.Null)
                    break
                i += 1

            # Option to decode the key. Bad idea if wanting to detect function keys such as 'Esc'.
            if decode:
                # Updates the _KeyPressEventListener
                self.Listener.invoke(self, KeyCodes.tostring(keycodes[0], keycodes[1]))
            elif keycodes[1] == b'\x00':
                # A key which can be represented as a single Unicode character
                self.Listener.invoke(self, keycodes[0])
            else:
                # A special function key that is represented as a combination of two Unicode characters
                self.Listener.invoke(self, keycodes[0], keycodes[1])
        else:
            keycode = self._getch()

            # Option to decode the key. Bad idea if wanting to detect function keys such as 'Esc'.
            if decode:
                keycode = keycode.decode('latin1')

            # Updates the _KeyPressEventListener
            self.Listener.invoke(self, keycode)


    class __UnixKeyPress:
        """
        Credits:
            https://code.activestate.com/recipes/134892/
        """

        def __init__(self):
            try:
                import tty, sys
            except ImportError as e:
                WriteShell("An error occurred while importing module '", e.name,
                           "' for KeyPressEventHandler initialization. Does this system lack the required module?",
                           sep='', stderr=True, Color='error', flush=True)

        def __call__(self):
            try:
                import sys
                import tty
                import termios

                stdin_file = sys.stdin.fileno()
                tty_attr = termios.tcgetattr(stdin_file)

                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            except ImportError as impEx:
                WriteShell("An error occurred while importing module '", impEx.name,
                           "' when calling KeyPressEventHandler. Does this system lack the required modules?",
                           sep='', stderr=True, Color='error', flush=True)
                return
            finally:
                import termios
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
            except ImportError as ex:
                WriteShell("An error occurred while importing module '", ex.name,
                           "' for KeyPressEventHandler initialization. Does this system lack the required module?",
                           sep='', stderr=True, Color='error', flush=True)

        def __call__(self):
            try:
                import msvcrt
                return msvcrt.getch()
            except ImportError as impEx:
                WriteShell("An error occurred while importing module '", impEx.name,
                           "' when calling KeyPressEventHandler. Does this system lack the required module?",
                           sep='', stderr=True, Color='error', flush=True)

#endregion KeyPressEventHandler
