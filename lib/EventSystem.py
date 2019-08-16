"""
.NET-style event system in Python
The aim of this module is to create an event system using only Python's base installation (e.g. no Anaconda, PyPy, etc.)
"""

if __name__ == "__main__":
    # MAJOR +1 represents an added function.
    __MAJOR = 2
    # MINOR +1 represents a change in existing function(s) within the current MAJOR.
    __MINOR = 0

    __info = """This file contains the module 'EventSystem', used to integrate event-driven functions.
To use this module in another project, include this file inside the project's directory."""

    print("========================================================")
    print("EventSystem.py version ", __MAJOR, ".", __MINOR, sep='', end='\n\n')
    print(__info)
    print("========================================================\n")
    input("Press enter to continue...")



#========================Imports========================

# no import



#========================Common Functions========================

# no function



#========================Template classes: EventArgs, EvenListener, EventHandler========================

class EventArgs:
    """
    Arguments for a generic event.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs



class EventListener:
    """
    Base class for implementing new event listeners.
    Event listener classes should be underscored (hidden).
    Listeners serve as an intermediary to an event handler and subscribed methods, implementing a custom EventArgs.
    """

    def __init__(self, *subscribers):
        # Subscribers (function delegates) to this event listener are stored here.
        self.Subscribers = []

        for method in subscribers:
            self += method


    def __iadd__(self, subscriber):
        if subscriber not in self.Subscribers:
            self.Subscribers.append(subscriber)


    def __len__(self):
        return len(self.Subscribers)


    def __repr__(self):
        s = str(type(self)) + "contains these subscribers:"
        for method in self.Subscribers:
            s += "\n    " + str(method)
        return s


    def notify(self, sender, args: EventArgs):
        """
        Notifies all subscribers when an event occurs.
        """

        for subscriber in self.Subscribers:
            subscriber(sender, args)



class EventHandler:
    """
    Handles the raising of an event.
    This class is the one which needs to be implemented in order to access the event system.
    """

    def __init__(self, listener: EventListener):
        self.Listener = listener


    def updatelistener(self, **kwargs):
        self.Listener.notify(self, EventArgs(**kwargs))



#========================Version History========================

# 1.0
"""
    Initial Release
    Crafted a basic version of an event system with base EventArgs, EventListener, and EventHandler classes.
        These classes are both a set of for implementing custom event system, and also a generic event system.
    Implemented a custom event system for detecting key presses.

    Additions
    ---------
        Base classes:
        -class EventArgs
            -__init__(self, **kwargs)
        -class EventListener
            -__init__(self, *subscribers)
            -notify(self, sender, args: EventArgs)
        -class EventHandler
            -__init__(self, listener: EventListener)
            -updatelistener(self, **kwargs)
        Detecting key presses:
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

# 1.1
"""
    Critical bug fix for user input event system.

    Bug Fixes
    ---------
        -KeyPressEventHandler.readkey() contains a critical bug
            -On certain Python distributions, calling 'msvcrt' module's getch() will only return one byte for normal
             ASCII characters. This is in contrast with the previous implementation, where a normal ASCII character
             is also considered as a combination character, with a second modifier byte as the null byte b'\x00'
            -Added code for detecting if the input is a normal character or not. Line 153
             If true, will abort the detection of a second modifier byte and return it as a null character byte.
            -NOTE: This module has not yet been tested on Unix-like systems, which has a different readkey() behaviour.
"""

# 2.0
"""
    Refactored EventSystem.py into different modules for better support of modular event creations.
    This file, EventSystem.py, contains the base template classes for creating event systems.
    Key input events have been migrated into EventSystem.KeyPress.py file.

    Changes
    -------
        -

    Bug Fixes
    ---------
        -Minor typo fixes.
"""
