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

def gen_mat(n):
    return np.zeros((n, n))

def gen_left_and_right(n):
    return (
        list(range(n))
        , list(range(n))
    )

def gen_init_options(n):
    return list(range(1, n - 1))

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

def nqueens(n):
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
            for skip in range(2, )
            for y in range(j, n, 2):
                traverse(i + 1, y + 2, [*tmp, (i, y)])

    for j in gen_init_options(n):
        traverse(1, j + 2, [(0, j)])

    return opts



test = [
    nqueens(i)
    for i in range(1, 5)
]
