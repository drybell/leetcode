"""
200. Number of Islands
https://leetcode.com/problems/number-of-islands/

Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.

Example 1:

Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1

Example 2:

Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3

Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 300
grid[i][j] is '0' or '1'.

Strategy:

Brute force search is TLE, need to find some optimizations

 v
[1,1,0,0,0,1,1]
[1,1,1,0,0,0,1]
[1,0,0,0,0,0,1]

check row and column find next 1 that supercedes a 0
or maybe check each one on row
 v
[1,1,0,0,0,1,1]
[1,
[1,

           v
[1,1,0,0,0,1,1]
           0
           0

   v
[1,1,0,0,0,1,1]
   1
   0
           v
[1,1,0,0,0,1,1]
           0
           0

     v
   >[1,1,0,0,0,1,1]
    [1,0,1,0,0,0,1]
    [1,0,0,0,0,0,1]

     v
   >[1,1,0,0,0,1,1]
    [1,
    [1,

               v
   >[1,1,0,0,0,1,1]
    [1,
    [1,

               v
   >[1,1,0,0,0,1,1]
               0
               0

     v
    [1,1,0,0,0,1,1]
   >[1,0,1,0,0,0,1]
    [1,0,0,0,0,0,1]

     v
    [1
   >[1,0,1,0,0,0,1]
    [1



1 1
1,1,1,0,0,0,1]
 ,0,0,0,0,0,1]



"""

from numislands_test import grid as testgrid

def num_islands(grid):
    width  = len(grid)
    height = len(grid[0])

    current    = 0

    def clamp(loc):
        x, y = loc
        return (
            max(min(x, width - 1), 0)
            , max(min(y, height - 1), 0)
        )

    def adjacent(x, y):
        return list(set(map(
            clamp
            , [
                (x + 1, y)
                , (x - 1, y)
                , (x, y + 1)
                , (x, y - 1)
                #, (x - 1, y - 1)
                #, (x + 1, y + 1)
                #, (x - 1, y + 1)
                #, (x + 1, y - 1)
            ]
        )))

    def adjacent_lands(x, y):
        locs = adjacent(x, y)
        lands = []

        for i, j in locs:
            if grid[i][j] == '1':
                lands.append((i, j))

        return lands

    def traverse_land(x, y):
        grid[x][y] = '0'
        [
            traverse_land(*land)
            for land in adjacent_lands(x, y)
        ]

    for x in range(width):
        if '1' not in grid[x]:
            continue

        y = grid[x].index('1')

        while y < height:
            if grid[x][y] == '1':
                current += 1
                traverse_land(x,y)
                if '0' not in grid[x][y + 1:]:
                    break

                y = grid[x][y + 1:].index('0') + y + 1
            else:
                if '1' not in grid[x][y + 1:]:
                    break

                y = grid[x][y + 1:].index('1') + y + 1

    return current

test = [
    num_islands([
      ["1","1","0","0","0"],
      ["1","1","0","0","0"],
      ["0","0","1","0","0"],
      ["0","0","0","1","1"]
    ])
    , num_islands([
      ["1","1","1","1","0"],
      ["1","1","0","1","0"],
      ["1","1","0","0","0"],
      ["0","0","0","0","0"]
    ])
    #, num_islands(testgrid)
]

"""
Thoughts:

Initial solution caused a TLE

I missed the trick of setting the visited node to 0,
reducing the search range by a significant amount
"""

"""
GRAVEYARD:

def num_islands(grid):
    width  = len(grid)
    height = len(grid[0])

    traversals = []
    current    = 0

    def clamp(loc):
        x, y = loc
        return (
            max(min(x, width - 1), 0)
            , max(min(y, height - 1), 0)
        )

    def adjacent(x, y):
        return list(set(map(
            clamp
            , [
                (x + 1, y)
                , (x - 1, y)
                , (x, y + 1)
                , (x, y - 1)
                #, (x - 1, y - 1)
                #, (x + 1, y + 1)
                #, (x - 1, y + 1)
                #, (x + 1, y - 1)
            ]
        )))

    def adjacent_lands(x, y):
        locs = adjacent(x, y)
        lands = []

        for i, j in locs:
            if (i, j) not in traversals and grid[i][j] == '1':
                lands.append((i, j))

        return lands

    def traverse_land(x, y):
        traversals.append((x, y))
        [
            traverse_land(*land)
            for land in adjacent_lands(x, y)
        ]

    for x in range(width):
        if '1' not in grid[x]:
            continue

        for y in range(height):
            if grid[x][y] == '1' and (x, y) not in traversals:
                current += 1
                traverse_land(x,y)

    return current
"""
