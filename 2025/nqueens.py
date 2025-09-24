"""
51. N-Queens

The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.

Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.

Example 1:

Input: n = 4
Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
Explanation: There exist two distinct solutions to the 4-queens puzzle as shown above

Example 2:

Input: n = 1
Output: [["Q"]]
"""

import numpy as np
from itertools import chain

def gen_mat(n):
    return np.zeros((n, n))

def gen_left_and_right(n):
    return (
        list(range(n))
        , list(range(n))
    )

def gen_init_options(n):
    if n <= 7:
        return list(range(
            0, n
        )) if n % 2 == 1 else list(range(
            1, n - 1
        ))
    else:
        return list(range(0, n))

def gen_diagonal(i, j, n):
    diag = [(i, j)]

    icopy = i
    jcopy = j

    while i - 1 >= 0 and j - 1 >= 0:
        j -= 1
        i -= 1
        diag.append((i, j))

    i = icopy
    j = jcopy

    while i + 1 < n and j + 1 < n:
        i += 1
        j += 1
        diag.append((i, j))

    i = icopy
    j = jcopy

    while i - 1 >= 0 and j + 1 < n:
        i -= 1
        j += 1
        diag.append((i, j))

    i = icopy
    j = jcopy

    while i + 1 < n and j - 1 >= 0:
        i += 1
        j -= 1
        diag.append((i, j))

    return diag

def short_notation(idxs):
    n = len(idxs)
    d = [None] * n
    for i, j in idxs:
        s = ['.'] * n
        s[j] = 'Q'
        d[i] = ''.join(s)

    return d

def long_notation(idxs):
    n = len(idxs)
    d = [None] * n
    for i, j in idxs:
        s = ['.'] * n
        s[j] = 'Q'
        d[i] = s

    return d

def yonly_notation(idxs):
    n = len(idxs)
    d = [None] * n
    for i, j in enumerate(idxs):
        s = ['.'] * n
        s[j] = 'Q'
        d[i] = s

    return d

def nqueensv1(n):
    if n == 1:
        return [["Q"]]
    if n in (2, 3):
        return []

    opts = []
    print()
    print(n)

    def traverse(left, right, tmp, exclude):
        if len(tmp) == n:
            opts.append(tmp)
            return exclude

        if not left and not right:
            return False

        if not tmp:
            l = list(left)
            l.pop(0)

            for y, j in enumerate(gen_init_options(n)):
                r = list(right)
                r.pop(j)
                print((0, j))

                traverse(
                    l, r
                    , [*tmp, (0, j)]
                    , [*exclude, *gen_diagonal(0, j, n)]
                )
        else:
            for x, i in enumerate(left):
                for y, j in enumerate(right):
                    if (i, j) in exclude:
                        continue
                    if opts and (i, j) in opts[-1]:
                        continue

                    l = list(left)
                    r = list(right)

                    l.pop(x)
                    r.pop(y)

                    traverse(
                        l, r
                        , [*tmp, (i, j)]
                        , [*exclude, *gen_diagonal(i, j, n)]
                    )

        return False

    traverse(*gen_left_and_right(n), [], [])
    return opts

def nqueens_exploration(n):
    if n == 1:
        return [["Q"]]
    if n in (2, 3):
        return []

    opts = []
    print()
    print(n)

    def traverse(i, j, tmp):
        if len(tmp) == n:
            opts.append(tmp)
            return

        if j >= n:
            for y in range(0, n - 2, 2):
                traverse(i + 1, y + 2, [*tmp, (i, y)])
        else:
            for y in range(j, n, 2):
                traverse(i + 1, y + 2, [*tmp, (i, y)])

    for j in gen_init_options(n):
        traverse(0, j + 2, [(0, j)])

    return opts

def generate_y_vals(n):
    skips = list(range(1, n))
    vals  = list(range(n))
    init  = gen_init_options(n)

    val = []
    curr = 0

    while init:
        curr = init.pop(0)
        val.append(curr)

        for skip in skips:
            while len(val) < n and (new := (val[-1] + skip) % n) not in val:
                val.append(new)

            if len(val) == n:
                yield val
                val = [curr]

def generate_skips(n):
    skips = list(range(2, n - 1))

    val = 0 if n % 2 == 1 else 1

    for skip in skips:
        for _ in range(n):
            val += skip
            yield val % n

def generate_alternating_skips(n):
    skips = list(range(2, n - 1))

    val = 0

    for _ in range(n):
        for skip in skips:
            val += skip
            yield val % n

def another_nqueens(n):
    if n == 1:
        return [["Q"]]
    if n in (2, 3):
        return []

    opts = []
    print()
    print(n)

    def traverse(i, j, skip, tmp):
        print(i, j, skip, tmp)
        if len(tmp) == n and tmp not in opts:
            opts.append(tmp)
            return

        if j + skip >= n:
            j = (j + skip) % n
        else:
            j += skip

        for newskip in range(1, n):
            for y in range(j, n, newskip):
                if y not in tmp and abs(y - tmp[-1]) != 1:
                    traverse(i + 1, y, newskip, [*tmp, y])

    for j in gen_init_options(n):
        for skip in range(2, n):
            traverse(1, j, skip, [j])

    return opts


def short_notation(idxs):
    n = len(idxs)
    d = [None] * n
    for i, j in enumerate(idxs):
        s = ['.'] * n
        s[j] = 'Q'
        d[i] = ''.join(s)

    return d

def nqueens(n):
    """
    The trick was to just create a disallow list
    by looking through the current y coordinates
    and adding left/right to the list based on
    how far away they are from the current index

    Q . . . . .  j = 0
    ^
    . . . . . .  at i = 1, (j + 1, j - 1) added to disallow
  ^   ^

    at i = 2, we extend Qi's previous reach + 1 since we
    are 2 away, and the previous by 1 since its 1 away

    Q . . . . .  j = 0
    . . Q . . .  j = 2
    . . . . . .
      ^ ^ ^
    """
    if n == 1:
        return [["Q"]]
    if n in (2, 3):
        return []

    opts = []

    def traverse(j, tmp):
        tmplen = len(tmp)

        if tmplen == n:
            opts.append(tmp)
            return

        disallowed = set(chain.from_iterable([
            ((prev - (tmplen - i))
            , (prev + (tmplen - i)))
            for i, prev in enumerate(tmp)
        ]))

        options = set(chain.from_iterable([
            (
                (j + skip) % n
                , abs(j - skip) % n
            )
            for skip in range(2, n)
        ]))

        for option in options:
            if option not in tmp and option not in disallowed:
                traverse(option, [*tmp, option])


    for j in gen_init_options(n):
        traverse(j, [j])

    return [
        short_notation(opt) for opt in opts
    ]


test = [
    nqueens(i)
    for i in range(1, 5)
]

"""
NQueens 5

[["Q....","..Q..","....Q",".Q...","...Q."],["Q....","...Q.",".Q...","....Q","..Q.."],[".Q...","...Q.","Q....","..Q..","....Q"],[".Q...","....Q","..Q..","Q....","...Q."],["..Q..","Q....","...Q.",".Q...","....Q"],["..Q..","....Q",".Q...","...Q.","Q...."],["...Q.","Q....","..Q..","....Q",".Q..."],["...Q.",".Q...","....Q","..Q..","Q...."],["....Q",".Q...","...Q.","Q....","..Q.."],["....Q","..Q..","Q....","...Q.",".Q..."]]
"""

"""
GRAVEYARD

def nqueens(n):
    if n == 1:
        return [["Q"]]
    if n in (2, 3):
        return []

    opts = []

    def traverse(j, tmp):
        if len(tmp) == n:
            opts.append(tmp)
            return

        options = [
            (
                (j + skip) % n
                , abs(j - skip) % n
            )
            for skip in range(2, n)
        ]

        for left, right in options:
            if left not in tmp:
                return traverse(left, [*tmp, left])
            if right not in tmp:
                return traverse(right, [*tmp, right])


    for j in gen_init_options(n):
        traverse(j, [j])

    return opts


"""
