"""UJS Escaped String Comparator.

Compares strings while normalizing Unicode escapes, JSON string escapes,
and backslash sequences to their logical values.
"""

from .core import normalize, compare, equals

__all__ = ["normalize", "compare", "equals"]
