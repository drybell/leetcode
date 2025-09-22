"""
37. Sudoku Solver
https://leetcode.com/problems/sudoku-solver/description/

Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:

Each of the digits 1-9 must occur exactly once in each row.
Each of the digits 1-9 must occur exactly once in each column.
Each of the digits 1-9 must occur exactly once in each of the 9 3x3 sub-boxes of the grid.
The '.' character indicates empty cells.


Example 1:
Input: board = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]

Output: [["5","3","4","6","7","8","9","1","2"],["6","7","2","1","9","5","3","4","8"],["1","9","8","3","4","2","5","6","7"],["8","5","9","7","6","1","4","2","3"],["4","2","6","8","5","3","7","9","1"],["7","1","3","9","2","4","8","5","6"],["9","6","1","5","3","7","2","8","4"],["2","8","7","4","1","9","6","3","5"],["3","4","5","2","8","6","1","7","9"]]

"""

from functools import reduce

opts = set([str(i) for i in range(1, 10)])

def handler(base, as_set=True):
    return base if not as_set else set(base)

def get_row(board, i, j, as_set=True):
    return handler([
        x for idx, x in enumerate(board[i])
        if x != '.'
    ], as_set)

def get_col(board, i, j, as_set=True):
    return handler([
        col[j] for idx, col in enumerate(board)
        if col[j] != '.'
    ], as_set)

def get_row_indexes(board, i, j, keep=False):
    return [
        (i, idx) for idx, x in enumerate(board[i])
        if x == '.' and (idx != j if not keep else True)
    ]

def get_col_indexes(board, i, j, keep=False):
    return [
        (idx, j) for idx, col in enumerate(board)
        if col[j] == '.' and (idx != i if not keep else True)
    ]

def get_bounds(idx):
    if 0 <= idx <= 2:
        return 0
    elif 3 <= idx <= 5:
        return 3
    else:
        return 6

def get_square_indexes(board, i, j, keep=False):
    x = get_bounds(i)
    y = get_bounds(j)

    return [
        (x_i, y_i)
        for x_i in range(x, x+3)
        for y_i in range(y, y+3)
        if board[x_i][y_i] == '.'
            and ((x_i, y_i) != (i, j) if not keep else True)
    ]

def get_unsolved_neighbors(board, i, j):
    return list(set([
        *get_square_indexes(board, i, j)
        , *get_row_indexes(board, i, j)
        , *get_col_indexes(board, i, j)
    ]))

def get_square(board, i, j, as_set=True):
    x = get_bounds(i)
    y = get_bounds(j)

    return handler([
        board[x_i][y_i]
        for x_i in range(x, x+3)
        for y_i in range(y, y+3)
        if board[x_i][y_i] != '.'
    ], as_set)

def available(board, i, j):
    return opts.difference((
        get_row(board, i, j)
        .union(get_col(board, i, j))
        .union(get_square(board, i, j))
    ))

def guess_option(board, cache, i, j):
    option = get_square(cache, i, j, False)

    current = [
        subset for subset in option
        if subset is not None
    ]

def is_solved(board):
    return all('.' not in b for b in board)

def update_cache(board, cache, i, j):
    cache[i][j] = available(board, i, j)

    if len(cache[i][j]) == 1:
        #print((i, j), cache[i][j])
        board[i][j] = cache[i][j].pop()
        #print('\n'.join(str(b) for b in board))
        #print()

        for neighbor in get_unsolved_neighbors(board, i, j):
            update_cache(board, cache, *neighbor)

def solve_simple(board, cache, init=True):
    while init or any(s is not None and len(s) == 1 for c in cache for s in c):
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val != '.':
                    continue

                update_cache(board, cache, i, j)

        init = False

def get_best_square(board):
    square_idxs = [
          (0, 0), (0, 3), (0, 6)
        , (3, 0), (3, 3), (3, 6)
        , (6, 0), (6, 3), (6, 6)
    ]

    squares = [
        get_square_indexes(
            board, *square_idx, keep=True
        )
        for square_idx in square_idxs
    ]

    smallest = 10
    res = []

    for i, sq in enumerate(squares):
        if 0 < (l := len(sq)) < smallest:
            smallest = l
            res = [i]
        elif l == smallest:
            res.append(i)

    return [(square_idxs[i], squares[i]) for i in res]

def solve_with_guess(board, cache):
    if is_solved(board):
        return cache, board

    cloned_board = [list(b) for b in board]
    cloned_cache = [list(c) for c in cache]

    for corner, square_idxs in get_best_square(cloned_board):
        current_available = [
            available(cloned_board, i, j)
            for i, j in square_idxs
        ]

        options = reduce(
            lambda x, y: x.union(y)
            , current_available
        )

        if not options:
            return False

        for option in options:
            ic, jc = square_idxs[0]
            #print(f'Try {option} on {(ic, jc)}')

            if option not in available(cloned_board, ic, jc):
                #print(f'Stale {option} on {(ic, jc)}')
                continue

            cloned_board[ic][jc] = option
            cloned_cache[ic][jc] = set()

            for neighbor in get_unsolved_neighbors(cloned_board, ic, jc):
                update_cache(cloned_board, cloned_cache, *neighbor)

            result = solve_with_guess(cloned_board, cloned_cache)

            if not result:
                #print(f'Failed with {option} on {(ic, jc)}')
                cloned_board = [list(b) for b in board]
                cloned_cache = [list(c) for c in cache]
            else:
                return result

def solve(board):
    cache = [[None] * 9 for _ in range(9)]

    solve_simple(board, cache)
    newcache, newboard = solve_with_guess(board, cache)

    for i, row in enumerate(newboard):
        for j, val in enumerate(row):
            board[i][j] = val

    return newcache, newboard


test = [
    solve(
        [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
    )
    , solve(
        [[".",".","9","7","4","8",".",".","."],["7",".",".",".",".",".",".",".","."],[".","2",".","1",".","9",".",".","."],[".",".","7",".",".",".","2","4","."],[".","6","4",".","1",".","5","9","."],[".","9","8",".",".",".","3",".","."],[".",".",".","8",".","3",".","2","."],[".",".",".",".",".",".",".",".","6"],[".",".",".","2","7","5","9",".","."]]
    )
    #, solve(
    #    [[".",".",".",".",".",".",".",".","."],[".","9",".",".","1",".",".","3","."],[".",".","6",".","2",".","7",".","."],[".",".",".","3",".","4",".",".","."],["2","1",".",".",".",".",".","9","8"],[".",".",".",".",".",".",".",".","."],[".",".","2","5",".","6","4",".","."],[".","8",".",".",".",".",".","1","."],[".",".",".",".",".",".",".",".","."]]
    #)
]

"""
GRAVEYARD

#common = reduce(
    #    lambda x, y: x.intersection(y)
    #    , current
    #)

    #if not common:
    #    return

    #diffs = [
    #    subset.difference(common)
    #    for subset in current
    #]

        square = [
            board[i][j]
            for i, j in get_square_indexes(
                board, *square_idx
            )
        ]
"""
