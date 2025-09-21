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

opts = set([str(i) for i in range(1, 10)])

def solve(board):
    def get_row(i, j):
        return set([
            x for idx, x in enumerate(board[i])
            if x != '.'
        ])

    def get_col(i, j):
        return set([
            col[j] for idx, col in enumerate(board)
            if col[j] != '.'
        ])

    def get_square(i, j):
        def get_bounds(idx):
            if 0 <= idx <= 2:
                return 0
            elif 3 <= idx <= 5:
                return 3
            else:
                return 6

        x = get_bounds(i)
        y = get_bounds(j)

        return set([
            board[x_i][y_i]
            for x_i in range(x, x+3)
            for y_i in range(y, y+3)
            if board[x_i][y_i] != '.'
        ])

    def available(i, j):
        return opts.difference((
            get_row(i, j)
            .union(get_col(i, j))
            .union(get_square(i, j))
        ))

    cache = [[None] * 9 for _ in range(9)]
    max_iters = 10
    iters = 0

    while any('.' in b for b in board) and iters < max_iters:
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val != '.':
                    continue

                cache[i][j] = available(i, j)

                if len(cache[i][j]) == 1:
                    board[i][j] = cache[i][j].pop()

        iters += 1

    return cache, board


test = [
    solve(
        [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
    )
    , solve(
        [[".",".","9","7","4","8",".",".","."],["7",".",".",".",".",".",".",".","."],[".","2",".","1",".","9",".",".","."],[".",".","7",".",".",".","2","4","."],[".","6","4",".","1",".","5","9","."],[".","9","8",".",".",".","3",".","."],[".",".",".","8",".","3",".","2","."],[".",".",".",".",".",".",".",".","6"],[".",".",".","2","7","5","9",".","."]]
    )
]
