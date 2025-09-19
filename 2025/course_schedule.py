"""
207. Course Schedule
https://leetcode.com/problems/course-schedule/description/

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return true if you can finish all courses. Otherwise, return false.

Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0. So it is possible.
Example 2:

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There are a total of 2 courses to take.
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.

Constraints:

1 <= numCourses <= 2000
0 <= prerequisites.length <= 5000
prerequisites[i].length == 2
0 <= ai, bi < numCourses
All the pairs prerequisites[i] are unique.

Strategy:

This seems to be generating a graph from the prerequisites list,
and if there are any cycles/loops detected then there is no
way to finish all.

There may be other scenarios, but looping is the only one
I can think of at the moment

Examples of Valid Prereqs

simple chain : linked-list style
0 -> 1 -> 2 -> 3

types of faults for simple chain: I believe none

dependency graph : nodes linking to a parent
0 -> 2 <- 1

types of faults for dependency graph: loops

0 <-> 1

or

0 -> 1 -> 2 -> 3
          ^    ^
               v
     4 -> 5 -> 6

this is almost a cycle, but this seems to be a valid
dependency graph

0 -> 1 -> 2 -> 3 -> 8
          ^    v    ^
     4 -> 5 -> 6 -> 7

I still think that looping is the only criteria for failure

Formally speaking, this looks to be detection of cycles in
a supposed DAG

Let's break down the translation step:

0 -> 1 -> 2 -> 3 -> 8
          ^    v    ^
     4 -> 5 -> 6 -> 7

8 <- 7 <- 6
8 <- 3
6 <- 5 <- 4
3 <- 2
2 <- 5 <- 4
2 <- 1 <- 0

converting each node to its nearest children we get
a list of stacks where stack_i represents the dependencies
of node i

[ [], [0], [5,1], [2], [], [4], [5], [6], [7,3] ]

I believe the goal would be to exhaust the dependency list
by tracing each stack's dependencies


[ [], [0], [5,1], [2], [], [4], [5], [6], [7,3] ]
            ^

let's pick node 2.

[5,1] -> stacks[5] -> [4] -> []
         stacks[1] -> [0] -> []

let's try 8 (the optimal)

[7,3] -> stacks[7] -> [6] -> [5]   -> [4] -> []
         stacks[3] -> [2] -> [5,1] -> stacks[5] -> [4] -> []
                                      stacks[1] -> [0] -> []

now let's try to add a loop and see how that goes

[ [], [0, 2], [1] ]

[0, 2] -> stacks[0] -> []
       -> stacks[2] -> [1] -> [0, 2]

[0, 2] == [0, 2] and loop is detected

problem now is defining the recursive operation and keeping
track of traversed nodes during a dependency sweep

"""


def can_finish(courses, prereqs):
    stacks = [[] for _ in range(courses)]

    for class_to_take, prereq in prereqs:
        stacks[class_to_take].insert(0, prereq)

    # if all class nodes require dependencies, then we can
    # immediately exit early since there will have to be loops
    if all(map(len, stacks)):
        return False

    while not all(map(len, stacks)):
        for i, stack in enumerate(stacks):
            if not stack:
                continue

            while stack:
                dep = stack.pop(0)



    return stacks

test = [
    can_finish(2, [[1,0]])
    , can_finish(2, [[1,0], [0,1]])
]

