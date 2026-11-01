import unittest

from ujs_escaped_string_comparator import normalize, compare, equals


class TestNormalize(unittest.TestCase):
    def test_plain_string(self):
        self.assertEqual(normalize("hello"), "hello")

    def test_json_escaped_newline(self):
        self.assertEqual(normalize("line1\\nline2"), "line1\nline2")

    def test_json_escaped_tab(self):
        self.assertEqual(normalize("a\\tb"), "a\tb")

    def test_json_escaped_quote(self):
        self.assertEqual(normalize('say \\"hi\\"'), 'say "hi"')

    def test_json_escaped_backslash(self):
        self.assertEqual(normalize("c:\\\\path"), "c:\\path")

    def test_unicode_escape(self):
        self.assertEqual(normalize("\\u0041"), "A")

    def test_unicode_escape_lowercase(self):
        self.assertEqual(normalize("\\u00e9"), "é")

    def test_mixed_escapes(self):
        self.assertEqual(normalize("tab:\\t newline:\\n unicode:\\u0041"), "tab:\t newline:\n unicode:A")

    def test_invalid_escape_preserved(self):
        # A backslash followed by a character that is not a valid JSON escape
        # should be left as-is (backslash and character both retained).
        self.assertEqual(normalize("a\\qb"), "a\\qb")

    def test_incomplete_unicode_escape(self):
        # Not enough hex digits: the backslash and 'u' are preserved.
        self.assertEqual(normalize("\\u12"), "\\u12")

    def test_invalid_unicode_escape(self):
        # Non-hex characters: the backslash and 'u' are preserved.
        self.assertEqual(normalize("\\uXYZW"), "\\uXYZW")

    def test_json_string_with_quotes(self):
        # If the input is already a quoted JSON string, it should be decoded
        # as such.
        self.assertEqual(normalize('"hello\\nworld"'), "hello\nworld")

    def test_empty_string(self):
        self.assertEqual(normalize(""), "")

    def test_only_backslash(self):
        # A lone backslash at the end of the string.
        self.assertEqual(normalize("\\"), "\\")


class TestCompare(unittest.TestCase):
    def test_equal_plain(self):
        self.assertTrue(compare("abc", "abc"))

    def test_not_equal_plain(self):
        self.assertFalse(compare("abc", "abd"))

    def test_equal_after_normalization(self):
        self.assertTrue(compare("a\\nb", "a\nb"))

    def test_not_equal_after_normalization(self):
        self.assertFalse(compare("a\\nb", "a\\tb"))

    def test_unicode_equivalence(self):
        self.assertTrue(compare("\\u0041", "A"))

    def test_invalid_escape_equivalence(self):
        # Both sides have the same invalid escape, so they are equal.
        self.assertTrue(compare("a\\qb", "a\\qb"))

    def test_invalid_escape_not_equal_to_decoded(self):
        # "a\\qb" normalizes to "a\\qb", while "aqb" normalizes to "aqb".
        # They are not equal.
        self.assertFalse(compare("a\\qb", "aqb"))

    def test_equals_alias(self):
        self.assertEqual(equals("a\\nb", "a\nb"), compare("a\\nb", "a\nb"))


if __name__ == "__main__":
    unittest.main()
