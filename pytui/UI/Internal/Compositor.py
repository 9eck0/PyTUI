"""
This file contains fast algorithms for string manipulation and concatenation, used for UI elements composition and
rendering.
"""


from typing import Sequence

import Color
from UI.Internal.ElementCanvas import ElementCanvas
from Utils.ComparisonTreeND import ComparisonTreeND
from Utils.MathHelper import clamp, quantize


#region Utility functions

def longest_list(lists: Sequence[Sequence]):
    return max(
        [len(i) for i in lists]
    )

#endregion


def infill_bounds(comp: list[str]):
    width = longest_list(comp)
    height = len(comp)


def concat_UI(base_frame: list[str], top_elem: list[str], x: int, y: int):
    """
    Inserts an UI element (component, or another frame) on top of a larger base frame.
    This function will limit the resulting composition to within the bounds of the base frame, cutting off parts
    of top_elem exceeding these bounds.

    :param base_frame: The bottom frame render.
    :param top_elem: The element to insert onto the base frame.
    :param x: The horizontal coordinate for insertion, incremental from left to right.
    :param y: The vertical coordinate for insertion, incremental from top to bottom.
    :return: The resulting UI render, as a list of lines/str.
    :rtype: list[str]
    """

    for i in range(x, len(base_frame[0])):
        pass


def concat_UI_strings(base_frame: str, top_elem: str, x: int, y: int):
    comp = base_frame.split('\n')
    insertion = top_elem.split('\n')
    return '\n'.join(concat_UI(comp, insertion, x, y))


#region ================================ Pattern-matching ================================


transparency_dither_full_blocks = {
    1.0: "█",
    0.75: "▓",
    0.5: "▚",
    0.25: "▒",
    0.2: "░",
    0.1: "▏"
}

_pattern_chars_quadrants_weights = [
    # Full blocks
    ('█', (1.00, 1.00, 1.00, 1.00)),            # Full block
    ('▓', (0.75, 0.75, 0.75, 0.75)),            # Dark shade
    ('▒', (0.25, 0.25, 0.25, 0.25)),            # Medium shade
    ('░', (0.20, 0.20, 0.20, 0.20)),            # Light shade
    # Vertical slices
    ('▀', (1.00, 1.00, 0.00, 0.00)),            # Upper half block
    ('▔', (0.00, 0.00, 0.00, 0.00)),            # Upper 1/8 block
    ('▁', (0.00, 0.00, 0.25, 0.25)),            # Lower 1/8 block
    ('▂', (0.00, 0.00, 0.50, 0.50)),            # Lower 1/4 block
    ('▃', (0.00, 0.00, 0.75, 0.75)),            # Lower 3/8 block
    ('▄', (0.00, 0.00, 1.00, 1.00)),            # Lower half block
    ('▆', (0.50, 0.50, 1.00, 1.00)),            # Lower 3/4 block
    ('▅', (0.25, 0.25, 1.00, 1.00)),            # Lower 5/8 block
    ('▇', (0.75, 0.75, 1.00, 1.00)),            # Lower 7/8 block
    # Horizontal slices
    ('▐', (0.00, 0.50, 0.00, 0.50)),            # Right half block
    ('▕', (0.00, 0.00, 0.00, 0.00)),            # Right 1/8 block
    ('▏', (0.25, 0.00, 0.25, 0.00)),            # Left 1/8 block
    ('▎', (0.50, 0.00, 0.50, 0.00)),            # Left 1/4 block
    ('▍', (0.75, 0.00, 0.75, 0.00)),            # Left 3/8 block
    ('▌', (1.00, 0.00, 1.00, 0.00)),            # Left half block
    ('▋', (1.00, 0.25, 1.00, 0.25)),            # Left 5/8 block
    ('▊', (1.00, 0.50, 1.00, 0.50)),            # Left 3/4 block
    ('▉', (1.00, 0.75, 1.00, 0.75)),            # Left 7/8 block
    # Quadrants
    ('▖', (0.00, 0.00, 1.00, 0.00)),            # Quadrant bl
    ('▗', (0.00, 0.00, 0.00, 1.00)),            # Quadrant br
    ('▘', (1.00, 0.00, 0.00, 0.00)),            # Quadrant tl
    ('▝', (0.00, 1.00, 0.00, 0.00)),            # Quadrant tr
    ('▚', (1.00, 0.00, 0.00, 1.00)),            # Quadrant tl, br
    ('▞', (0.00, 1.00, 1.00, 0.00)),            # Quadrant tr, bl
    ('▙', (1.00, 0.00, 1.00, 1.00)),            # Quadrant tl, bl, br
    ('▛', (1.00, 1.00, 1.00, 0.00)),            # Quadrant tl, tr, bl
    ('▜', (1.00, 1.00, 0.00, 1.00)),            # Quadrant tl, tr, br
    ('▟', (0.00, 1.00, 1.00, 1.00)),            # Quadrant tr, bl, br
    # Obliques
    ('◢', (0.00, 0.50, 0.50, 1.00)),            #
    ('◣', (0.50, 0.00, 1.00, 0.50)),            #
    ('◤', (1.00, 0.50, 0.50, 0.00)),            #
    ('◥', (0.50, 1.00, 0.00, 0.50)),            #
    ('/', (0.00, 0.25, 0.25, 0.00)),            # Forward slash
    ('\\',(0.25, 0.00, 0.00, 0.25)),            # Backslash
    ('|', (0.10, 0.10, 0.10, 0.10))            #
    #('', (0.00, 0.00, 0.00, 0.00))             #
]
"""
Unicode rendering character quadrant weights distribution.
Earlier entries (i.e. at the top of list) are prioritized when building the LUT.

The values stored are the true integer percentages of the character shapes.
Quantization should not occur within this data.
"""

_pattern_weights_granularity = 0x2

_pattern_chars_lut = {
    0xFFFF: ("█", False)
}
"""
Rapid look-up table (LUT) for Unicode character pattern-matching, with schema as follows: \n
"0x[tl][tr][bl][br] : (character, is_reverse)",
where each quadrant in square brackets is encoded as a nibble value (i.e. single hexadecimal digit).

Patterns stored in this LUT are the closest Unicode character matches for a specific combination of quadrant weights
as percentage numbers from 0 to 100.
Reverse patterns are also present, indicated by the second boolean output.
Call _populate_pattern_chars_lut() to rebuild this LUT.

Trades memory usage for performance, as the lookup operation becomes ~O(1) instead of O(N).
This is necessary for real-time TUI rendering within pure Python.
"""


def _weight_to_nibble(weight: float, granularity: int):
    return clamp(0,
                 quantize(clamp(0.0, weight, 1.0) * 0xF, granularity),
                 0xF)


def _quadrants_to_hex(tl: float, tr: float, bl: float, br: float):
    return \
        _weight_to_nibble(tl, _pattern_weights_granularity) * 0x1000 + \
        _weight_to_nibble(tr, _pattern_weights_granularity) * 0x100 + \
        _weight_to_nibble(bl, _pattern_weights_granularity) * 0x10 + \
        _weight_to_nibble(br, _pattern_weights_granularity)


def _populate_pattern_chars_lut():
    """
    Internal function to populate all possible value levels of Unicode chars LUT with the charset in the weights list.

    Note that the higher the granularity (i.e. the lower the value of _pattern_weights_granularity), the larger the
    look-up table becomes.
    """

    # Intermediate/temporary comparison trees for fast mapping & seeking
    imap = ComparisonTreeND(None, (0.5, 0.5, 0.5, 0.5))
    reverse_imap = ComparisonTreeND(None, (0.5, 0.5, 0.5, 0.5))

    # Populate temporary comparison trees
    for char, weights in _pattern_chars_quadrants_weights:
        if any(weights):
            # Store char pattern weights and its reverse. Prioritize original (non-reversed) pattern when possible.
            imap.add(char, weights, overwrite=False)
            reverse_weights = [1-w for w in weights]
            if any(reverse_weights):
                reverse_imap.add(char, reverse_weights, overwrite=False)

    # Granularity-based steppings for the LUT table
    lut_steps = list(range(0, 0x10, _pattern_weights_granularity))
    if 0xF not in lut_steps:
        lut_steps.append(0xF)
    # Normalize to [0, 1]
    lut_steps = [x/0xF for x in lut_steps]

    for tl in lut_steps:
        for tr in lut_steps:
            for bl in lut_steps:
                for br in lut_steps:
                    # Quantize weights according to granularity.
                    vec = (tl, tr, bl, br)
                    lut_key = _quadrants_to_hex(*vec)
                    
                    # Compare between original and reverse patterns to determine the closest likeliness
                    orig_node = imap.seek(vec, True)
                    rev_node = reverse_imap.seek(vec, True)
                    if orig_node.distance(vec) <= rev_node.distance(vec):
                        # Append original pattern to current LUT position
                        _pattern_chars_lut[lut_key] = (orig_node.value, False)
                    else:
                        # Append reverse pattern to current LUT position
                        _pattern_chars_lut[lut_key] = (rev_node.value, True)

_populate_pattern_chars_lut()


def match_to_char(tl: float, tr: float, bl: float, br: float):
    """
    Match a raster pattern to the closest Unicode character.

    The raster pattern provided needs to be divided into four quadrants and be provided as percentage area for each
    quadrant. The pattern division only supports distinguishing between two colors (text foreground and background).

    :param tl: A float value between 0 and 1 representing the area of the pattern occupying the top-left quadrant.
    :param tr: A float value between 0 and 1 representing the area of the pattern occupying the top-right quadrant.
    :param bl: A float value between 0 and 1 representing the area of the pattern occupying the bottom-left quadrant.
    :param br: A float value between 0 and 1 representing the area of the pattern occupying the bottom-right quadrant.
    :return: Two values:
    1) A Unicode character with a close match to the raster pattern provided.
    2) Whether the returned character is the reversed pattern (i.e. swap bg and fg colors).
    """

    lut_key = _quadrants_to_hex(tl, tr, bl, br)
    return _pattern_chars_lut[lut_key]


"""
# Test LUT dict using match-to-char
x = input()
while x != '':
    y = [float(c.strip()) for c in x.split(',')]
    print(match_to_char(*y))
    x = input()
"""


def dither_color(fg_color: Color, bg_color: Color):
    pass


def dither(color: Color, ):
    """
    Dithers

    The dithering algorithm generates complex variations based on the color gradient and

    :param color:
    :return:
    """


#endregion


def render_color(elem: ElementCanvas):
    pass


