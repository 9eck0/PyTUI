"""
Common mathematical functions from PyTUI.
"""


import math
from typing import SupportsFloat, SupportsIndex, Any


def clamp(floor, value, ceil):
    """
    Limits (clamps) a value between two inclusive extrema.

    :param floor: The lower limit.
    :param value: The value to clamp.
    :param ceil: The upper limit.
    :return: The clamped value.
    """
    floor, ceil = min(floor, ceil), max(floor, ceil)
    return min(max(floor, value), ceil)


def norm(*comp: SupportsFloat | SupportsIndex):
    """
    Calculates the norm (length) of a given vector with given components.

    :param comp: The components of the vector.
    :return: The vector's norm.
    """
    return math.pow(sum([math.pow(x, 2) for x in comp]), 0.5)


def quantize(number, granularity):
    """
    Rounds a number to within a given discrete precision.

    Example:
      number=11, granularity=3;     result=12
      number=11, granularity=-7;   result=14
      number=-11, granularity=7;   result=-14

    :param number: The number to quantize.
    :param granularity: The granularity, or divisor
    :return: The quantized number, as int.
    """
    return int(round(number / granularity) * granularity)


def sign(*numbers):
    """
    Returns the sign of a list of numbers.
    Alternatively, this function can be though of as finding the unit vectors of a given vector.

    :param numbers: A list of numbers.
    :return: A list of unit integers (either -1, 0 or 1).
    """
    return tuple([0 if x == 0 else int(x//abs(x)) for x in numbers])
