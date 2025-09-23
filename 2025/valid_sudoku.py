"""
36. Valid Sudoku
https://leetcode.com/problems/valid-sudoku/

Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:

Each row must contain the digits 1-9 without repetition.
Each column must contain the digits 1-9 without repetition.
Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.
Note:

A Sudoku board (partially filled) could be valid but is not necessarily solvable.
Only the filled cells need to be validated according to the mentioned rules.

Strategy:

Simply create functions for the 3 scenarios, along with
methods to iterate through the board
"""

import numpy as np

def convert_to_mat(board):
    return np.array([
        [int(i) if i != '.' else -1 for i in row]
        for row in board
    ])

def is_subarray_unique(arr):
    return arr[arr != -1].shape[0] == len(set(arr[arr != -1]))

def apply_along_rows(board):
    return np.apply_along_axis(is_subarray_unique, 1, board).all()

def apply_along_cols(board):
    return np.apply_along_axis(is_subarray_unique, 0, board).all()

def apply_along_squares(board):
    return np.array([
        is_subarray_unique(board[i:i+3, j:j+3].flatten())
        for i in range(0, 9, 3)
        for j in range(0, 9, 3)
    ]).all()

def is_valid_sudoku(board):
    b = convert_to_mat(board)

    return (
        apply_along_rows(b)
        and apply_along_cols(b)
        and apply_along_squares(b)
    )

test = [
    is_valid_sudoku([
        ["5","3",".",".","7",".",".",".","."]
        ,["6",".",".","1","9","5",".",".","."]
        ,[".","9","8",".",".",".",".","6","."]
        ,["8",".",".",".","6",".",".",".","3"]
        ,["4",".",".","8",".","3",".",".","1"]
        ,["7",".",".",".","2",".",".",".","6"]
        ,[".","6",".",".",".",".","2","8","."]
        ,[".",".",".","4","1","9",".",".","5"]
        ,[".",".",".",".","8",".",".","7","9"]
    ])
]

"""
Notes:

not the fastest or the most optimal solution,
but showcases simplicity of breaking the problem into parts
and using numpy to solve each step

May revisit this to solve without numpy at some point
"""

def check_rows(board):
    return np.apply_along_axis(is_subarray_unique, 1, board)

def check_cols(board):
    return np.apply_along_axis(is_subarray_unique, 0, board)

def check_squares(board):
    return np.array([
        is_subarray_unique(board[i:i+3, j:j+3].flatten())
        for i in range(0, 9, 3)
        for j in range(0, 9, 3)
    ])

def check_sudoku(board):
    b = convert_to_mat(board)
    return [
        check_rows(b)
        , check_cols(b)
        , check_squares(b)
    ]

