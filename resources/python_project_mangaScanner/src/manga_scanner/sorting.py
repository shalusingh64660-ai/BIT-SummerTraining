from __future__ import annotations
import re
"""Sorting helpers for manga page filenames."""




def natural_sort_key(value: str) -> tuple[object, ...]:
    """Return a key that sorts embedded numbers numerically.

    Example:
        ``page2.png`` should sort before ``page10.png``.

    TODO: Split the string into text and digit chunks. Lowercase text chunks,
    convert digit chunks to integers, and return them as a tuple.
    """
    parts = re.split(r"(\d+)", value)

    result = []

    for part in parts:
        if part.isdigit():
            result.append(int(part))
        else:
            result.append(part.lower())

    return tuple(result)

    raise NotImplementedError("TODO: implement natural_sort_key")