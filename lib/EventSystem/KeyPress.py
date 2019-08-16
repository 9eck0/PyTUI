"""
.NET-style event system in Python
The aim of this module is to create an event system using only Python's base installation (e.g. no Anaconda, PyPy, etc.)
"""

if __name__ == "__main__":
    # MAJOR +1 represents an added function.
    __MAJOR = 1
    # MINOR +1 represents a change in existing function(s) within the current MAJOR.
    __MINOR = 0

    __info = """This file contains the module 'KeyEvent', used to integrate key press events.
To use this module in another project, include this file inside the project's directory."""

    print("========================================================")
    print("KeyPress.py version ", __MAJOR, ".", __MINOR, sep='', end='\n\n')
    print(__info)
    print("========================================================\n")
    input("Press enter to continue...")



#========================Imports========================

# Used by:
import os

from lib.Utils import *
from lib.EventSystem import *



#========================Common Functions========================

# no function



#========================KeyPressEvent classes: KeyPressEventArgs, _KeyPressEventListener, KeyPressEventHandler========================

class KeyPressEventArgs(EventArgs):

    def __init__(self, key, key2=b'\x00', **kwargs):
        EventArgs.__init__(self, **kwargs)
        self.Key = key
        self.Key2 = key2
        if key2 == b'\x00':
            self.isSpecialKey = False
        else:
            self.isSpecialKey = True



class KeyPressEventListener(EventListener):

    def __init__(self, *subscribers):
        EventListener.__init__(self, *subscribers)


    def notify(self, sender, key, key2=b'\x00'):
        """
        Notifies all subscribers about a key press.

        Args:
            sender:
            key:
            key2:
        """

        EventListener.notify(self, sender, KeyPressEventArgs(key, key2))



class KeyPressEventHandler(EventHandler):

    def __init__(self, *subscribers):

        if os.name == 'nt':
            self._getch = KeyPressEventHandler.__WindowsKeyPress()
        else:       # fallback method. Most likely os.name == 'posix'
            self._getch = KeyPressEventHandler.__UnixKeyPress()

        EventHandler.__init__(self, KeyPressEventListener(*subscribers))


    def readkey(self, decode=False):
        """
        Updates methods and functions subscribed to this event handler.
        Any subscriber must implement the exact parameters: subscriber(sender, args: KeyPressEventArgs)
            where parameter 'args' contains the string character mapped from the pressed key.

        Args:
            decode: Whether to decode the key code into the corresponding character.
        """

        if os.name == 'nt':
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
                i+=1

            # Option to decode the key. Bad idea if wanting to detect function keys such as 'Esc'.
            if decode:
                # Updates the _KeyPressEventListener
                self.Listener.notify(self, KeyCodes.tostring(keycodes[0], keycodes[1]))
            elif keycodes[1] == b'\x00':
                # A key which can be represented as a single Unicode character
                self.Listener.notify(self, keycodes[0])
            else:
                # A special function key that is represented as a combination of two Unicode characters
                self.Listener.notify(self, keycodes[0], keycodes[1])
        else:
            keycode = self._getch()

            # Option to decode the key. Bad idea if wanting to detect function keys such as 'Esc'.
            if decode:
                keycode = keycode.decode('latin1')

            # Updates the _KeyPressEventListener
            self.Listener.notify(self, keycode)


    class __UnixKeyPress:
        """
        Credits:
            http://code.activestate.com/recipes/134892/
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
                import sys, tty, termios
                stdin_file  = sys.stdin.fileno()
                tty_attr = termios.tcgetattr(stdin_file)

                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            except ImportError as impE:
                WriteShell("An error occurred while importing module '", impE.name,
                           "' when calling KeyPressEventHandler. Does this system lack the required modules?",
                           sep='', stderr=True, Color='error', flush=True)
            finally:
                termios.tesetattr(stdin_file, termios.TCSADRAIN, tty_attr)

            return ch



    class __WindowsKeyPress:
        """
        Credits:
            http://code.activestate.com/recipes/134892/
        """

        def __init__(self):
            try:
                import msvcrt
            except ImportError as e:
                WriteShell("An error occurred while importing module '", e.name,
                           "' for KeyPressEventHandler initialization. Does this system lack the required module?",
                           sep='', stderr=True, Color='error', flush=True)

        def __call__(self):
            try:
                import msvcrt
                return msvcrt.getch()
            except ImportError as impE:
                WriteShell("An error occurred while importing module '", impE.name,
                           "' when calling KeyPressEventHandler. Does this system lack the required module?",
                           sep='', stderr=True, Color='error', flush=True)



class KeyCodes:
    """
    This class contains bytecodes of common unicode characters.
    """

    # For special function keys, Python's msvcrt module will return this prefix, followed by the function key's bytecode
    FunctionPrefix = b'\xe0'

    Null = b'\x00'
    Backspace = b'\x08'
    BackspaceChar = b'\x7f'     # For legacy purposes; deprecated
    Escape = b'\x1b'
    Enter = b'\n'               # Ctrl + Enter/Return or Ctrl + J
    Return = b'\r'              # Enter/Return or Ctrl + M
    Tab = b'\t'                 # Tab or Ctrl + I

    CtrlZ = b'\x1a'             # Undo
    CtrlX = b'\x18'             # Cut
    CtrlC = b'\x03'             # Copy
    CtrlV = b'\x16'             # Paste
    CtrlB = b'\x02'             # Embolden
    CtrlN = b'\x0e'             # New Item
    CtrlM = Return

    CtrlA = b'\x01'             # Select All
    CtrlS = b'\x13'             # Save Item
    CtrlD = b'\x04'
    CtrlF = b'\x06'             # Find
    CtrlG = b'\x07'
    CtrlH = b'\x08'
    CtrlJ = Enter
    CtrlK = b'\x0b'
    CtrlL = b'\x0c'

    CtrlQ = b'\x11'             # Quit
    CtrlW = b'\x17'
    CtrlE = b'\x05'             # Center
    CtrlR = b'\x12'
    CtrlT = b'\x14'
    CtrlY = b'\x19'             # Redo
    CtrlU = b'\x15'             # Underline
    CtrlI = Tab
    CtrlO = b'\x0f'             # Open Item
    CtrlP = b'\x10'             # Print

    Zero = b'0'
    One = b'1'
    Two = b'2'
    Three = b'3'
    Four = b'4'
    Five = b'5'
    Six = b'6'
    Seven = b'7'
    Eight = b'8'
    Nine = b'9'

    CommercialAt = b'@'
    NumberSign = b'#'
    DollarSign = b'$'
    PercentSign = b'%'
    Caret = b'^'
    Ampersand = b'&'
    Grave = b'`'
    Tilde = b'~'

    Space = b' '
    ExclamationMark = b'!'
    QuestionMark = b'?'
    QuotationMark = b'"'
    Apostrophe = b"'"
    Comma = b','
    Period = b'.'
    Colon = b':'
    Semicolon = b';'

    LeftParenthesis = b'('
    RightParenthesis = b')'
    LeftBracket = b'['
    RightBracket = b']'
    LeftCurlyBracket = b'{'
    RightCurlyBracket = b'}'
    LeftAngleBracket = b'<'
    RightAngleBracket = b'>'

    Add = b'+'
    Subtract = b'-'
    Asterisk = b'*'
    Slash = b'/'
    Backslash = b'\\'
    Equal = b'='
    Underscore = b'_'

    A = b'A'
    B = b'B'
    C = b'C'
    D = b'D'
    E = b'E'
    F = b'F'
    G = b'G'
    H = b'H'
    I = b'I'
    J = b'J'
    K = b'K'
    L = b'L'
    M = b'M'
    N = b'N'
    O = b'O'
    P = b'P'
    Q = b'Q'
    R = b'R'
    S = b'S'
    T = b'T'
    U = b'U'
    V = b'V'
    W = b'W'
    X = b'X'
    Y = b'Y'
    Z = b'Z'

    a = b'a'
    b = b'b'
    c = b'c'
    d = b'd'
    e = b'e'
    f = b'f'
    g = b'g'
    h = b'h'
    i = b'i'
    j = b'j'
    k = b'k'
    l = b'l'
    m = b'm'
    n = b'n'
    o = b'o'
    p = b'p'
    q = b'q'
    r = b'r'
    s = b's'
    t = b't'
    u = b'u'
    v = b'v'
    w = b'w'
    x = b'x'
    y = b'y'
    z = b'z'

    CombinationCharacters = {(FunctionPrefix, H) : 'ArrowUp',
                             (FunctionPrefix, P) : 'ArrowDown',
                             (FunctionPrefix, K) : 'ArrowLeft',
                             (FunctionPrefix, M) : 'ArrowRight',
                             (Null, Semicolon) : 'F1',
                             (Null, LeftAngleBracket) : 'F2',
                             (Null, Equal) : 'F3',
                             (Null, RightAngleBracket) : 'F4',
                             (Null, QuestionMark) : 'F5',
                             (Null, CommercialAt) : 'F6',
                             (Null, A) : 'F7',
                             (Null, B) : 'F8',
                             (Null, C) : 'F9',
                             (Null, D) : 'F10',
                             (FunctionPrefix, b'\x85') : 'F11',
                             (FunctionPrefix, b'\x86') : 'F12',
                             (FunctionPrefix, R) : 'Insert',
                             (FunctionPrefix, S) : 'Del',
                             (FunctionPrefix, I) : 'PageUp',
                             (FunctionPrefix, Q) : 'PageDown',
                             (FunctionPrefix, G) : 'Home',
                             (FunctionPrefix, O) : 'End',
                             (Null, CtrlC) : 'Ctrl+2'}

    @staticmethod
    def tostring(key1: bytes, key2: bytes=b'\x00'):
        """
        Returns the string representation of

        Args:
            key1: The first bytecode returned from a keypress
            key2: The second bytecode returned from a keypress

        Returns:

        """

        # Those are normal characters, simply decode to their respective string literals
        if key2 == b'\x00':
            return key1.decode('latin1')
        else:
            return KeyCodes.CombinationCharacters[(key1, key2)]



#========================Version History========================

# 1.0
"""
    Initial Release
    Refactored from EventSystem.
    See version history from EventSystem.py

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