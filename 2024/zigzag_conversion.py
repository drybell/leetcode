"""
The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)

P   A   H   N
A P L S I I G
Y   I   R

And then read line by line: "PAHNAPLSIIGYIR"

Write the code that will take a string and make this conversion given a number of rows:

string convert(string s, int numRows);

Example 1:

Input: s = "PAYPALISHIRING", numRows = 3
Output: "PAHNAPLSIIGYIR"

Example 2:

Input: s = "PAYPALISHIRING", numRows = 4
Output: "PINALSIGYAHRPI"

Explanation:
P     I    N
A   L S  I G
Y A   H R
P     I

Example 3:

Input: s = "A", numRows = 1
Output: "A"


PAYPALISHIRING (3 rows)
___|___|___|__|
X   X   X   X |
 O O O O O O O|
  L   L   L   |

READS XXXXOOOOOOOLLL

so basically, given num_rows, we're looking to split up the
contents of the string based on an offset

easy case is row 1, which is static for all rowcounts

given a string of size N, the top row will always be:
    range(0, N, num_rows + 1)

the bottom row is also static, but with an offset:
    range(0 + (num_rows - 1), N, num_rows + 1)

the middle row is the tough part.

PAYPALISHIRING (4 rows)
____||____||__
X     X     X   <- the offset is now 5 apart, because the zig zag took
 O   O O   O O     an extra letter for the additional row
  o o   o o   |
   L     L

2 rows -> 0 diagonal
3 rows -> 1 diagonal
4 rows -> 2 diagonals
5 rows -> 3 diagonals?
N rows -> N - 2 diagonals

P       H
A     S I
Y   I   R
P L     I G
A       N


PAYPALISHIRING
_____|||_____|
X       X
 O     O O
  o   o   o
   . .     . .
    ^       ^

0       8      <-- 0, N, num_rows + (num_rows - 2)
 1     7 9
  2   6  10
   3 5    11 13
    4       12 <-- 0 + num_rows - 1, N, num_rows + (num_rows - 2)

now do we want to just +/- the indices every row iteration to
get the next values?

Example:
    0 -> 1, 8 -> 7, 9

    0 is easy, it's a left anchor,
    but 8 is hard to identify that we need
    to do both a + and - op

0, 8
1, 7, 9       diff_pattern = 6, 2, 6, 2, ...
2, 6, 10      diff_pattern = 4, 4, 4, 4, ...
3, 5, 11, 13  diff_pattern = 2, 6, 2, 6, ...


What about 10 rows?

0---    18    ---18
 1---   16   ---17   diff_pattern = 16, 2, 16, 2, ...
  2---  14  ---16    diff_pattern = 14, 4, 14, 4, ...
   3--- 12 ---15     diff_pattern = 12, 6, 12, 6, ...
    4-- 10 --14
     5-  8 -13
      6  6 12
       7  11
        810
         9

basically the pair of differences between the two indices
must add up to:
    (2 * num_rows) - 2

and reduces in size by 2

given num rows = N, for any row J the difference will be:

    (2N - 2) - 2J, 2J


"""


def prob(s : str, numRows : int) -> str:
    N = len(s)
    n = numRows

    if n == 1:
        return s

    magic_zz = n + n - 2

    top_anchor = list(range(        0, N, magic_zz))
    bot_anchor = list(range(0 + n - 1, N, magic_zz))

    def offset_gen(J):
        tmp = []
        curr = J
        while curr < N:
            tmp.append(curr)

            if len(tmp) % 2 == 0:
                curr += 2 * J
            else:
                curr += magic_zz - (2 * J)

        return tmp

    for i in range(1, n - 1):
        top_anchor += offset_gen(i)

    return ''.join(s[val] for val in top_anchor + bot_anchor)


def old_version(s, numRows):
    N = len(s)
    n = numRows

    if n == 1:
        return s

    magic_zz = n + n - 2

    top_anchor = list(range(        0, N, magic_zz))
    bot_anchor = list(range(0 + n - 1, N, magic_zz))

    inner = []

    def offset_gen(J):
        tmp = []
        curr = J
        while curr < N:
            tmp.append(curr)

            if len(tmp) % 2 == 0:
                curr += 2 * J
            else:
                curr += magic_zz - (2 * J)

        return tmp

    for i in range(1, n - 1):
        inner.append(offset_gen(i))

    return ''.join([s[val] for l in [top_anchor, *inner, bot_anchor] for val in l])
