"""
165. Compare Version Numbers
https://leetcode.com/problems/compare-version-numbers/description

Given two version strings, version1 and version2, compare them. A version string consists of revisions separated by dots '.'. The value of the revision is its integer conversion ignoring leading zeros.

To compare version strings, compare their revision values in left-to-right order. If one of the version strings has fewer revisions, treat the missing revision values as 0.

Return the following:

If version1 < version2, return -1.
If version1 > version2, return 1.
Otherwise, return 0.

Example 1:
Input: version1 = "1.2", version2 = "1.10"

Output: -1

Explanation:

version1's second revision is "2" and version2's second revision is "10": 2 < 10, so version1 < version2.

Example 2:
Input: version1 = "1.01", version2 = "1.001"

Output: 0

Explanation:

Ignoring leading zeroes, both "01" and "001" represent the same integer "1".

Example 3:
Input: version1 = "1.0", version2 = "1.0.0.0"

Output: 0

Explanation:

version1 has less revisions, which means every missing revision are treated as "0".


Constraints:

1 <= version1.length, version2.length <= 500
version1 and version2 only contain digits and '.'.
version1 and version2 are valid version numbers.
All the given revisions in version1 and version2 can be stored in a 32-bit integer.
"""

def compare_versions(v1, v2):
    maxlen = max(len(v1.split('.')), len(v2.split('.')))

    def gen_next_number(v):
        for num in v.split('.'):
            yield int(num)

        while True:
            yield 0

    for i, (number1, number2) in enumerate(zip(
        gen_next_number(v1), gen_next_number(v2)
    )):
            if number1 < number2:
                return -1
            elif number1 > number2:
                return 1
            elif i == maxlen:
                return 0

    return 0

test = [
    compare_versions('1.2', '1.10')
    , compare_versions('1.01', '1.001')
    , compare_versions('1.0', '1.0.0.0')
    , compare_versions('1.0', '1.0.1')
]
