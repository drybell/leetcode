"""
529. Minesweeper

https://leetcode.com/problems/minesweeper/

Let's play the minesweeper game (Wikipedia, online game)!

You are given an m x n char matrix board representing the game board where:

'M' represents an unrevealed mine,
'E' represents an unrevealed empty square,
'B' represents a revealed blank square that has no adjacent mines (i.e., above, below, left, right, and all 4 diagonals),
digit ('1' to '8') represents how many mines are adjacent to this revealed square, and
'X' represents a revealed mine.
You are also given an integer array click where click = [clickr, clickc] represents the next click position among all the unrevealed squares ('M' or 'E').

Return the board after revealing this position according to the following rules:

If a mine 'M' is revealed, then the game is over. You should change it to 'X'.
If an empty square 'E' with no adjacent mines is revealed, then change it to a revealed blank 'B' and all of its adjacent unrevealed squares should be revealed recursively.
If an empty square 'E' with at least one adjacent mine is revealed, then change it to a digit ('1' to '8') representing the number of adjacent mines.
Return the board when no more squares will be revealed.

"""

def update(board, click):
    width  = len(board)
    height = len(board[0])

    check = set()

    def clamp(loc):
        x, y = loc

        return (
            min(max(x, 0), width - 1)
            , min(max(y, 0), height - 1)
        )

    def get_adjacent(x, y):
        return list(set(map(
            clamp, [
                (x + 1, y)
                , (x - 1, y)
                , (x, y + 1)
                , (x, y - 1)
                , (x + 1, y + 1)
                , (x - 1, y - 1)
                , (x + 1, y - 1)
                , (x - 1, y + 1)
            ]
        )))

    def get_adjacent_mines(i, j):
        mines = []
        locs = []
        for (x, y) in get_adjacent(i, j):
            match board[x][y]:
                case 'M':
                    mines.append((x, y))
                case 'E':
                    locs.append((x, y))

        return mines, locs

    def reveal(x, y):
        if x < 0 or y < 0 or x >= width or y >= height:
            return

        match board[x][y]:
            case 'E':
                mines, locs = get_adjacent_mines(x, y)

                if mines:
                    board[x][y] = str(len(mines))

                else:
                    board[x][y] = 'B'

                    [reveal(*loc) for loc in locs]

    x, y = click

    if board[x][y] == 'M':
        board[x][y] = 'X'
        return board

    reveal(x, y)
    return board

test = [
    #update([["E","E","E","E","E"],["E","E","M","E","E"],["E","E","E","E","E"],["E","E","E","E","E"]], [3,0])
    update([["E","E","E","E","E","E","E","E"],["E","E","E","E","E","E","E","M"],["E","E","M","E","E","E","E","E"],["M","E","E","E","E","E","E","E"],["E","E","E","E","E","E","E","E"],["E","E","E","E","E","E","E","E"],["E","E","E","E","E","E","E","E"],["E","E","M","M","E","E","E","E"]], [0,0])
    , update([["B","B","B","B","B","B","1","E"],["B","1","1","1","B","B","1","M"],["1","2","M","1","B","B","1","1"],["M","2","1","1","B","B","B","B"],["1","1","B","B","B","B","B","B"],["B","B","B","B","B","B","B","B"],["B","1","2","2","1","B","B","B"],["B","1","M","M","1","B","B","B"]], [0,7])
]

"""
GRAVEYARD

for some reason I got hung up on where to move a
digit tile back to unexplored, but realized I
didn't shove the reveal block only on blank explores

    def should_be_unexplored(i, j):
        if not board[i][j].isdigit():
            return

        locs = get_adjacent(i, j)
        store = 0

        for (x, y) in locs:
            curr = board[x][y]
            if curr.isdigit() or curr == 'M':
                store += 1

        if store == len(locs) and board[i][j] != 'M':
            board[i][j] = 'E'


"""
