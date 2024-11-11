import re

# Improved regular expression
expression = r"a(a*|b*)a"

# Test strings
test_strings = ["aa", "aaa", "aba", "abba", "a", "b", "aab", "ab"]

# Find matches
for test in test_strings:
    if re.fullmatch(expression, test):
        print(f"'{test}' matches the expression.")
    else:
        print(f"'{test}' does not match the expression.")
