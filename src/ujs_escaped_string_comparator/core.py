import json
import re

__all__ = ["normalize", "compare", "equals"]

# Matches a backslash followed by a single character that is not a valid
# JSON escape. We use this to detect backslash sequences that should be
# treated as literal backslashes rather than escape sequences.
_INVALID_JSON_ESCAPE = re.compile(r"\\(?![\"\\/bfnrtu])")

# Matches a JSON unicode escape sequence (\uXXXX).
_UNICODE_ESCAPE = re.compile(r"\\u([0-9a-fA-F]{4})")


def normalize(s):
    """Return the logical value of *s* after decoding escape sequences.

    The function first attempts to parse *s* as a JSON string literal. If that
    succeeds, the decoded string is returned. This handles all JSON escapes
    including \\uXXXX, \\n, \\t, etc.

    If *s* is not a valid JSON string literal (for example, it contains a
    backslash that is not part of a valid escape), we fall back to a
    best-effort decoding: valid JSON escapes are decoded and invalid
    backslash sequences are left as-is (backslash preserved). This matches
    the intuitive behaviour of treating a lone backslash as a literal
    character.

    This function is deterministic and has no side effects.
    """
    try:
        # json.loads requires a string that is a valid JSON value. A JSON
        # string literal must be enclosed in double quotes. We add them if
        # they are not already present.
        if not (s.startswith('"') and s.endswith('"')):
            s_quoted = '"' + s + '"'
        else:
            s_quoted = s
        return json.loads(s_quoted)
    except json.JSONDecodeError:
        # Not a valid JSON string literal. Fall back to manual decoding.
        return _manual_normalize(s)


def _manual_normalize(s):
    """Decode valid JSON escapes, leave invalid backslash sequences intact."""
    result = []
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if ch == '\\' and i + 1 < n:
            nxt = s[i + 1]
            if nxt in '"\\/':
                result.append(nxt)
                i += 2
                continue
            elif nxt == 'b':
                result.append('\b')
                i += 2
                continue
            elif nxt == 'f':
                result.append('\f')
                i += 2
                continue
            elif nxt == 'n':
                result.append('\n')
                i += 2
                continue
            elif nxt == 'r':
                result.append('\r')
                i += 2
                continue
            elif nxt == 't':
                result.append('\t')
                i += 2
                continue
            elif nxt == 'u' and i + 5 < n:
                hex_digits = s[i + 2 : i + 6]
                if all(c in '0123456789abcdefABCDEF' for c in hex_digits):
                    code_point = int(hex_digits, 16)
                    result.append(chr(code_point))
                    i += 6
                    continue
            # Invalid escape: keep the backslash and the next character
            result.append(ch)
            i += 1
        else:
            result.append(ch)
            i += 1
    return ''.join(result)


def compare(s1, s2):
    """Compare two strings after normalizing escape sequences.

    Returns True if the normalized forms are equal, False otherwise.
    """
    return normalize(s1) == normalize(s2)


def equals(s1, s2):
    """Alias for compare."""
    return compare(s1, s2)
