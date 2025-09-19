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
    nodes  = set()

    for class_to_take, prereq in prereqs:
        if prereq == class_to_take:
            return False

        stacks[class_to_take].insert(0, prereq)
        nodes.add(class_to_take)

    if len(nodes) == courses:
        return False

    def traverse(node, curr):
        if node not in nodes:
            return True

        if node in curr:
            return False

        curr.insert(0, node)

        for new in stacks[node]:
            if not traverse(new, curr):
                return False

            nodes.discard(new)

            if curr:
                curr.pop(-1)

        nodes.discard(node)

        return True

    for i in range(courses):
        if i not in nodes:
            continue

        if not traverse(i, []):
            return False

    return True

test = [
    can_finish(2, [[1,0]])
    , can_finish(2, [[1,0], [0,1]])
    , can_finish(20, [[0,10],[3,18],[5,5],[6,11],[11,14],[13,1],[15,1],[17,4]])
    , can_finish(3, [[1,0],[1,2],[0,1]])
    , can_finish(5, [[1,4],[2,4],[3,1],[3,2]])
    , can_finish(4, [[0,1],[3,1],[1,3],[3,2]])
    , can_finish(100, [[6,27],[83,9],[10,95],[48,67],[5,71],[18,72],[7,10],[92,4],[68,84],[6,41],[82,41],[18,54],[0,2],[1,2],[8,65],[47,85],[39,51],[13,78],[77,50],[70,56],[5,61],[26,56],[18,19],[35,49],[79,53],[40,22],[8,19],[60,56],[48,50],[20,70],[35,12],[99,85],[12,75],[2,36],[36,22],[21,15],[98,1],[34,94],[25,41],[65,17],[1,56],[43,96],[74,57],[19,62],[62,78],[50,86],[46,22],[10,13],[47,18],[20,66],[83,66],[51,47],[23,66],[87,42],[25,81],[60,81],[25,93],[35,89],[65,92],[87,39],[12,43],[75,73],[28,96],[47,55],[18,11],[29,58],[78,61],[62,75],[60,77],[13,46],[97,92],[4,64],[91,47],[58,66],[72,74],[28,17],[29,98],[53,66],[37,5],[38,12],[44,98],[24,31],[68,23],[86,52],[79,49],[32,25],[90,18],[16,57],[60,74],[81,73],[26,10],[54,26],[57,58],[46,47],[66,54],[52,25],[62,91],[6,72],[81,72],[50,35],[59,87],[21,3],[4,92],[70,12],[48,4],[9,23],[52,55],[43,59],[49,26],[25,90],[52,0],[55,8],[7,23],[97,41],[0,40],[69,47],[73,68],[10,6],[47,9],[64,24],[95,93],[79,66],[77,21],[80,69],[85,5],[24,48],[74,31],[80,76],[81,27],[71,94],[47,82],[3,24],[66,61],[52,13],[18,38],[1,35],[32,78],[7,58],[26,58],[64,47],[60,6],[62,5],[5,22],[60,54],[49,40],[11,56],[19,85],[65,58],[88,44],[86,58]])
    , can_finish(7, [[1,0],[0,3],[0,2],[3,2],[2,5],[4,5],[5,6],[2,4]])
]


"""
Notes:

I know that this problem requires knowing topological sort,
but I wanted to come to the efficient solution myself. After
learning about Kahn's algorithm, it looks like the solution
is similar to what I came up with in the end. I utilized the
fact that nodes that have no dependencies are nodes that
we want to resolve others to, so whenever we resolve a node
completely to non-dependent node, it means that that node is
resolved as well. we can continue this recursively until the
nodes set is empty.

For Kahn's algorithm, the process is similar, but instead
the focus reversed: choosing nodes that have no incoming
edges (nodes that have dependencies but are not dependent on
others). This approach is more "bottom-up", and resolves by
returning a sorted list that allows us to take the actions
in the appropriate order.

Kahn's algorithm:
L ← Empty list that will contain the sorted elements
S ← Set of all nodes with no incoming edge

while S is not empty do
    remove a node n from S
    add n to L
    for each node m with an edge e from n to m do
        remove edge e from the graph
        if m has no other incoming edges then
            insert m into S

if graph has edges then
    return error   (graph has at least one cycle)
else
    return L   (a topologically sorted order)

"""

"""
GRAVEYARD

def can_finish(courses, prereqs):
    print()
    stacks = [[] for _ in range(courses)]

    for class_to_take, prereq in prereqs:
        stacks[class_to_take].insert(0, prereq)

    print(stacks)

    # if all class nodes require dependencies, then we can
    # immediately exit early since there will have to be loops
    if all(map(len, stacks)):
        return False

    def traverse(node, origin, seen):
        print(f"start {node} {origin}")
        if node in seen:
            print(f'{node} in {seen}')
            return True

        if seen and origin and stacks[node] == origin:
            print(f'{stacks[node]} = {origin}')
            return False

        seen.append(node)

        for new_node in stacks[node]:
            print(f'traverse {new_node} -> {stacks[new_node]}')
            if not traverse(new_node, origin, seen):
                return False

        print(f"final {seen}")

        return True

    for i in range(courses):
        seen = []

        if i in stacks[i]:
            return False

        if not traverse(i, stacks[i], seen):
            return False

    return True

def can_finish(courses, prereqs):
    stacks = [[] for _ in range(courses)]

    for class_to_take, prereq in prereqs:
        stacks[class_to_take].insert(0, prereq)

    print()
    print(stacks)

    # if all class nodes require dependencies, then we can
    # immediately exit early since there will have to be loops
    if all(map(len, stacks)):
        return False

    seen = []

    def traverse(node, origin):
        print(node, origin, seen)

        if node in seen:
            print(f"{node} in {seen}")
            return False

        seen.append(node)

        if origin and stacks[node] == origin:
            print(f"{node} == {origin}")
            return False

        for newnode in stacks[node]:
            print(f"traverse {newnode} -> {stacks[newnode]}")
            if not traverse(newnode, origin):
                return False

        print(f"final {node} {seen}")

        return True

    for i in range(courses):
        if i in seen:
            continue

        for node in stacks[i]:
            if not traverse(node, stacks[i]):
                return False

    return True

TLE:
def can_finish(courses, prereqs):
    stacks = [[] for _ in range(courses)]

    for class_to_take, prereq in prereqs:
        stacks[class_to_take].insert(0, prereq)

    # if all class nodes require dependencies, then we can
    # immediately exit early since there will have to be loops
    if all(map(len, stacks)):
        return False

    seen = []

    def traverse(node, origin):
        if i in seen:
            return True

        seen.append(node)

        if stacks[node] == origin:
            return False

        for newnode in stacks[node]:
            if not traverse(newnode, origin):
                return False

        return True

    for i in range(courses):
        if i in seen:
            continue

        for node in stacks[i]:
            if not traverse(node, stacks[i]):
                return False

    return True
"""
