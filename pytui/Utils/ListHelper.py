"""
Generic functions for lists/collections manipulations.
"""


from typing import Sequence


def longest_list_length(lists: Sequence[Sequence]):
    return max(
        [len(i) for i in lists]
    )


def longest_list(lists: Sequence[Sequence]):
    return lists[longest_list_length(lists)]

