# ujs-escaped-string-comparator

Compares strings while normalizing Unicode escapes, JSON string escapes, and backslash sequences to their logical values.

## Usage

```python
from ujs_escaped_string_comparator import normalize, compare, equals

# Normalize a string containing escape sequences
normalize("hello\\nworld")  # returns "hello\nworld"
normalize("\\u0041")        # returns "A"

# Compare two strings after normalization
compare("a\\nb", "a\nb")    # returns True
equals("a\\nb", "a\nb")     # returns True (alias for compare)
```

## Why this library exists

The problem: when data travels through different layers (URLs, JSON, logs), the same logical string can be represented with different escape sequences. For example, a newline might appear as a literal newline, as `\n`, or as `\u000a`. Comparing the raw strings fails even though the intended content is identical.

This library decodes escape sequences to their logical values before comparing. The trade-off: we treat any string that is not a valid JSON string literal as a sequence of characters where valid JSON escapes are decoded and invalid backslash sequences are preserved as-is. This means a lone backslash before an ordinary character is kept, which is the least surprising behaviour for strings that are not strictly JSON.

## Edge case

A backslash followed by a character that is not a valid JSON escape (e.g., `\q`) is left untouched: both the backslash and the character are preserved. This avoids silently dropping characters when the input is not valid JSON.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

## Limitations

Values are coerced to floats, so very large integers lose precision. If you need
exact integer aggregates over a window, this is the wrong tool.

