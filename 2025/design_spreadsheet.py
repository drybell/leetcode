"""
3484. Design Spreadsheet
https://leetcode.com/problems/design-spreadsheet
https://leetcode.com/problems/design-spreadsheet/description/?envType=daily-question&envId=2025-09-19

A spreadsheet is a grid with 26 columns (labeled from 'A' to 'Z') and a given number of rows. Each cell in the spreadsheet can hold an integer value between 0 and 105.

Implement the Spreadsheet class:

Spreadsheet(int rows) Initializes a spreadsheet with 26 columns (labeled 'A' to 'Z') and the specified number of rows. All cells are initially set to 0.
void setCell(String cell, int value) Sets the value of the specified cell. The cell reference is provided in the format "AX" (e.g., "A1", "B10"), where the letter represents the column (from 'A' to 'Z') and the number represents a 1-indexed row.
void resetCell(String cell) Resets the specified cell to 0.
int getValue(String formula) Evaluates a formula of the form "=X+Y", where X and Y are either cell references or non-negative integers, and returns the computed sum.
Note: If getValue references a cell that has not been explicitly set using setCell, its value is considered 0.

Example 1:

Input:
["Spreadsheet", "getValue", "setCell", "getValue", "setCell", "getValue", "resetCell", "getValue"]
[[3], ["=5+7"], ["A1", 10], ["=A1+6"], ["B2", 15], ["=A1+B2"], ["A1"], ["=A1+B2"]]

Output:
[null, 12, null, 16, null, 25, null, 15]

Explanation

Spreadsheet spreadsheet = new Spreadsheet(3); // Initializes a spreadsheet with 3 rows and 26 columns
spreadsheet.getValue("=5+7"); // returns 12 (5+7)
spreadsheet.setCell("A1", 10); // sets A1 to 10
spreadsheet.getValue("=A1+6"); // returns 16 (10+6)
spreadsheet.setCell("B2", 15); // sets B2 to 15
spreadsheet.getValue("=A1+B2"); // returns 25 (10+15)
spreadsheet.resetCell("A1"); // resets A1 to 0
spreadsheet.getValue("=A1+B2"); // returns 15 (0+15)

Constraints:

1 <= rows <= 10**3
0 <= value <= 10**5
The formula is always in the format "=X+Y", where X and Y are either valid cell references or non-negative integers with values less than or equal to 105.
Each cell reference consists of a capital letter from 'A' to 'Z' followed by a row number between 1 and rows.
At most 104 calls will be made in total to setCell, resetCell, and getValue.

Notes:
pretty straightforward, just have to be able to parse the formula
and use a dict for efficient gets/sets. Initial approach used inner
lists to track the rows, but for space efficiency it was better
to use an inner dictionary and only track cells that were actually
modified since all others would be automatically set to 0.

This problem would have been a lot more interesting if the inputs
were not always properly configured, or to allow invalid cell
accesses/sets, etc.

"""

from string import ascii_uppercase

MAX_ROWS  = 10**3
MAX_VALUE = 10**5

class ManagerV1:
    def __init__(self, rows):
        self.data = {
            letter: [0 for _ in range(rows)]
            for letter in ascii_uppercase
        }

    def parse_cell(self, cell):
        return (
            (None, int(cell))
            if cell.isdigit() else
            (cell[0], int(cell[1:]))
        )

    def get(self, cell, index):
        if cell is None:
            return index

        return self.data[cell][index - 1]

    def set(self, cell, value):
        letter, index = self.parse_cell(cell)

        self.data[letter][index - 1] = value

    def reset(self, cell):
        self.set(cell, 0)

    def exec(self, formula):
        x, _, y = formula[1:].partition("+")

        vals = []
        for cell in [x, y]:
            vals.append(self.get(*self.parse_cell(cell)))

        return sum(vals)

class Manager:
    def __init__(self, rows):
        self.data = {
            letter: {}
            for letter in ascii_uppercase
        }

    def parse_cell(self, cell):
        return (
            (None, int(cell))
            if cell.isdigit() else
            (cell[0], int(cell[1:]))
        )

    def get(self, cell, index):
        if cell is None:
            return index

        return self.data[cell].get(index - 1, 0)

    def set(self, cell, value):
        letter, index = self.parse_cell(cell)

        self.data[letter][index - 1] = value

    def reset(self, cell):
        self.set(cell, 0)

    def exec(self, formula):
        x, _, y = formula[1:].partition("+")

        vals = []
        for cell in [x, y]:
            vals.append(self.get(*self.parse_cell(cell)))

        return sum(vals)



class Spreadsheet:

    def __init__(self, rows: int):
        self.inner = Manager(rows)

    def setCell(self, cell: str, value: int) -> None:
        return self.inner.set(cell, value)

    def resetCell(self, cell: str) -> None:
        return self.inner.reset(cell)

    def getValue(self, formula: str) -> int:
        return self.inner.exec(formula)


def executor(ids, args):
    results = []
    tm = Spreadsheet(args[0][0])

    print("EXECUTING")
    print(tm)

    for identifier, arg in zip(ids[1:], args[1:]):
        match identifier:
            case 'setCell':
                tm.setCell(*arg)
            case 'resetCell':
                tm.resetCell(*arg)
            case 'getValue':
                results.append(tm.getValue(*arg))

        print(identifier, arg)
        print(tm)
        print()

    return results, tm

test = [
    executor(
        ["Spreadsheet", "getValue", "setCell", "getValue", "setCell", "getValue", "resetCell", "getValue"]
        , [[3], ["=5+7"], ["A1", 10], ["=A1+6"], ["B2", 15], ["=A1+B2"], ["A1"], ["=A1+B2"]]
    )
]
