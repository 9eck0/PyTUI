"""
This file contains bytecodes of common ASCII characters present on a
standard culture-agnostic keyboard.
They are used to correspond with terminal systems running on Microsoft Windows.

Unsupported keys entry must be custom-handled using the returned bytecodes.
"""
from typing import Collection


#region ================================ KeyCodes ================================

class KeyCodes:
    """
    This class contains bytecodes of common ASCII characters returned by the Windows OS.
    """

    # For special function keys, Python's msvcrt module will return this prefix, followed by the function key's bytecode
    FunctionPrefix = b'\xe0'

    Null = b'\x00'

    # Editing keys

    Backspace = b'\x08'
    BackspaceChar = b'\x7f'     # For legacy purposes; deprecated
    Escape = b'\x1b'
    Enter = b'\n'               # Ctrl + Enter/Return or Ctrl + J
    """ Ctrl + Enter/Return or Ctrl + J """
    Return = b'\r'              # Enter/Return or Ctrl + M
    """ Enter/Return or Ctrl + M """
    Tab = b'\t'                 # Tab or Ctrl + I
    """ Tab or Ctrl + I """

    # Command modifier keys

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

    # Character keys

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

    # Function keys

    ArrowUp = (FunctionPrefix, H)
    ArrowDown = (FunctionPrefix, P)
    ArrowLeft = (FunctionPrefix, K)
    ArrowRight = (FunctionPrefix, M)

    F1 = (Null, Semicolon)
    F2 = (Null, LeftAngleBracket)
    F3 = (Null, Equal)
    F4 = (Null, RightAngleBracket)
    F5 = (Null, QuestionMark)
    F6 = (Null, CommercialAt)
    F7 = (Null, A)
    F8 = (Null, B)
    F9 = (Null, C)
    F10 = (Null, D)
    F11 = (FunctionPrefix, b'\x85')
    F12 = (FunctionPrefix, b'\x86')

    Insert = (FunctionPrefix, R)
    Del = (FunctionPrefix, S)
    PageUp = (FunctionPrefix, I)
    PageDown = (FunctionPrefix, Q)
    Home = (FunctionPrefix, G)
    End = (FunctionPrefix, O)

    Ctrl2 = (Null, CtrlC)

    CombinationCharacters = {(FunctionPrefix, H):       'ArrowUp',
                             (FunctionPrefix, P):       'ArrowDown',
                             (FunctionPrefix, K):       'ArrowLeft',
                             (FunctionPrefix, M):       'ArrowRight',
                             (Null, Semicolon):         'F1',
                             (Null, LeftAngleBracket):  'F2',
                             (Null, Equal):             'F3',
                             (Null, RightAngleBracket): 'F4',
                             (Null, QuestionMark):      'F5',
                             (Null, CommercialAt):      'F6',
                             (Null, A):                 'F7',
                             (Null, B):                 'F8',
                             (Null, C):                 'F9',
                             (Null, D):                 'F10',
                             (FunctionPrefix, b'\x85'): 'F11',
                             (FunctionPrefix, b'\x86'): 'F12',
                             (FunctionPrefix, R):       'Insert',
                             (FunctionPrefix, S):       'Del',
                             (FunctionPrefix, I):       'PageUp',
                             (FunctionPrefix, Q):       'PageDown',
                             (FunctionPrefix, G):       'Home',
                             (FunctionPrefix, O):       'End',
                             (Null, CtrlC):             'Ctrl+2'}

    @staticmethod
    def tostring(key1: bytes, key2: bytes = b'\x00'):
        """
        Returns a human-readable name of a keypress capture.

        Args:
            key1: The first bytecode returned from a keypress
            key2: The second bytecode returned from a keypress

        Returns:
            A descriptive string name of the specified key(s).
        """

        if key2 == KeyCodes.Null:
            # Those are normal characters, simply decode to their respective string literals
            return key1.decode('latin1')
        else:
            return KeyCodes.CombinationCharacters[(key1, key2)]

#endregion

#region ================================ KeyCombo ================================

class KeyCombo:
    """
    Represents an unordered and unique combination keys, serving to validate functional
    key presses/keyboard shortcuts.

    The stored combination can either be a single key value, or multiple keys given as
    a collection object.
    """

    def __init__(self, *combination: bytes | Collection[bytes]):
        self.key_combos = set()
        for x in combination:
            self.__iadd__(x)

    def __call__(self, *keycode: bytes):
        for combo in self.key_combos:
            if combo == keycode:
                # Singular bytes
                return True
            elif isinstance(combo, Collection):
                # Combination keys
                if set(combo) == set(keycode) and len(combo) == len(keycode):
                    return True
        return False

    def __contains__(self, item):
        if isinstance(item, Collection):
            return list(item) in self.key_combos
        else:
            return item in self.key_combos

    def __eq__(self, other):
        if isinstance(other, KeyCombo):
            return self.key_combos == other.key_combos
        elif isinstance(other, bytes):
            return self(other)      # __call__ for evaluation
        elif isinstance(other, Collection):
            return self(*other)     # __call__ for evaluation
        return False

    def __iadd__(self, other):
        if isinstance(other, bytes):
            self.key_combos += other
        elif isinstance(other, Collection):
            self.key_combos += list(other)
        else:
            raise ValueError(f"Attempting to add invalid value type ({type(other)}) to KeyCombo: {other}.")

    def __isub__(self, other):
        if isinstance(other, bytes) or isinstance(other, Collection):
            self.key_combos -= other
        else:
            raise ValueError(f"Attempting to remove invalid value type ({type(other)}) from KeyCombo: {other}.")

    def __len__(self):
        return len(self.key_combos)

    def __str__(self):
        readable_keycodes = []
        for key in self.key_combos:
            if isinstance(key, Collection):
                readable_keycodes += KeyCodes.tostring(*key)
            else:
                readable_keycodes += KeyCodes.tostring(key)
        return f"{{{", ".join(readable_keycodes)}}}"

#endregion
