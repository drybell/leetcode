"""
3408. Design Task Manager

There is a task management system that allows users to manage their tasks, each associated with a priority. The system should efficiently handle adding, modifying, executing, and removing tasks.

Implement the TaskManager class:

TaskManager(vector<vector<int>>& tasks) initializes the task manager with a list of user-task-priority triples. Each element in the input list is of the form [userid, taskid, priority], which adds a task to the specified user with the given priority.

void add(int userid, int taskid, int priority) adds a task with the specified taskid and priority to the user with userid. It is guaranteed that taskid does not exist in the system.

void edit(int taskid, int new_priority) updates the priority of the existing taskid to new_priority. It is guaranteed that taskid exists in the system.

void rmv(int taskid) removes the task identified by taskid from the system. It is guaranteed that taskid exists in the system.

int execTop() executes the task with the highest priority across all users. If there are multiple tasks with the same highest priority, execute the one with the highest taskid. After executing, the taskid is removed from the system. Return the userid associated with the executed task. If no tasks are available, return -1.

Note that a user may be assigned multiple tasks.

Example 1:

Input:
["TaskManager", "add", "edit", "execTop", "rmv", "add", "execTop"]
[[[[1, 101, 10], [2, 102, 20], [3, 103, 15]]], [4, 104, 5], [102, 8], [], [101], [5, 105, 15], []]

Output:
[null, null, null, 3, null, null, 5]

Explanation

TaskManager taskManager = new TaskManager([[1, 101, 10], [2, 102, 20], [3, 103, 15]]); // Initializes with three tasks for Users 1, 2, and 3.
taskManager.add(4, 104, 5); // Adds task 104 with priority 5 for User 4.
taskManager.edit(102, 8); // Updates priority of task 102 to 8.
taskManager.execTop(); // return 3. Executes task 103 for User 3.
taskManager.rmv(101); // Removes task 101 from the system.
taskManager.add(5, 105, 15); // Adds task 105 with priority 15 for User 5.
taskManager.execTop(); // return 5. Executes task 105 for User 5.

Constraints:

1 <= tasks.length <= 10^5
0 <= userid <= 10^5
0 <= taskid <= 10^5
0 <= priority <= 10^9
0 <= new_priority <= 10^9
At most 2 * 105 calls will be made in total to add, edit, rmv, and execTop methods.
The input is generated such that taskid will be valid.

Strategy:

My initial thought was to use priority queues, but the problem
is that we can't edit the specific elements in the queue on the
fly, which means we'll have to add another data structure to
let us update tasks efficiently.

Maybe we can have something that tracks the reference to the data
passed into the priority queue that lets us modify it?

For now I'll just use a min/max heap from `heapq` so I can peek
at the underlying list data and work through the naive solution

I was also thinking about using a B-Tree for this, which will
allow us to have efficient search/mutation/deletion of the data,
but I don't know if there's a standard module we can use. I may
have to attempt to implement a BTree to get this or look for
other solutions

First attempt is an obvious TLE, the mutations are all O(n),
and we need them to be most likely O(logn).

Second attempt was to convert the get operation of a TaskMaxHeap
from a list search into a combination of heap pops into puts,
making the get operation a delete as well. I don't think the
time complexity changes here at worst case scenarios, so the result
will most likely be another TLE, but useful for practice with heapq

Last attempt involved looking for a hint, which was in the `heapq`
docs specifying that we can faux-perserve the heap properties
by utilizing a garbage token and not actually removing the
data from the heap until we need to actually produce a result

"""

import json

from queue import PriorityQueue
import heapq

MAX_PRIORITY_ID = 10**9
MAX_TASK_ID     = 10**5

class TaskMaxHeapV1:

    def __init__(self):
        self.heap = []

    def add(self, item):
        priority, task, user = item

        heapq.heappush(
            self.heap
            , (
                MAX_PRIORITY_ID - priority
                , MAX_TASK_ID - task
                , user
            )
        )

    def get(self, taskid):
        for idx, (priority, task, user) in enumerate(self.heap):
            if task == (MAX_TASK_ID - taskid):
                return idx

    def edit(self, taskid, new_priority):
        idx = self.get(taskid)
        (priority, task, user) = self.heap[idx]

        self.heap[idx] = (
            MAX_PRIORITY_ID - new_priority
            , task
            , user
        )

        heapq.heapify(self.heap)

    def pop(self):
        if not self.heap:
            return -1

        return heapq.heappop(self.heap)

    def delete(self, taskid):
        idx = self.get(taskid)
        self.heap.pop(idx)
        heapq.heapify(self.heap)

class TaskMaxHeapV2:

    def __init__(self):
        self.heap = []

    def add(self, item):
        priority, task, user = item

        heapq.heappush(
            self.heap
            , (
                MAX_PRIORITY_ID - priority
                , MAX_TASK_ID - task
                , user
            )
        )

    def get(self, taskid):
        cache = []
        found = None

        while self.heap:
            curr = heapq.heappop(self.heap)

            if curr[1] == (MAX_TASK_ID - taskid):
                found = curr
                break
            else:
                cache.insert(0, curr)

        while cache:
            heapq.heappush(self.heap, cache.pop(0))

        return found

    def edit(self, taskid, new_priority):
        (priority, task, user) = self.get(taskid)

        heapq.heappush(
            self.heap
            , (
                MAX_PRIORITY_ID - new_priority
                , task
                , user
            )
        )

    def pop(self):
        if not self.heap:
            return -1

        return heapq.heappop(self.heap)

    def delete(self, taskid):
        self.get(taskid)


class Task:
    def __init__(self, priority, task, user):
        self.priority = priority
        self.task = task
        self.user = user

    def __ge__(self, other):
        return (self.priority, self.task) >= (other.priority, other.task)

    def __le__(self, other):
        return (self.priority, self.task) <= (other.priority, other.task)

    def __lt__(self, other):
        return (self.priority, self.task) < (other.priority, other.task)

    def __gt__(self, other):
        return (self.priority, self.task) > (other.priority, other.task)

    def __eq__(self, other):
        if isinstance(other, int):
            return False

        return (self.priority, self.task, self.user) == (other.priority, other.task, other.user)

    def __ne__(self, other):
        return (self.priority, self.task, self.user) != (other.priority, other.task, other.user)

class TaskMaxHeapV3:

    def __init__(self):
        self.heap     = []
        self.tracking = {}

    def add(self, item):
        priority, task, user = item

        taskid     = MAX_TASK_ID - task
        priorityid = MAX_PRIORITY_ID - priority

        self.tracking[task] = Task(priorityid, taskid, user)

        heapq.heappush(
            self.heap
            , self.tracking[task]
        )

    def get(self, taskid):
        return self.tracking[taskid]

    def edit(self, taskid, new_priority):
        self.get(taskid).priority = MAX_PRIORITY_ID - new_priority

        heapq.heapify(self.heap)

    def pop(self):
        if not self.heap:
            return -1

        popped = heapq.heappop(self.heap)
        return self.tracking.pop(MAX_TASK_ID - popped.task)

    def delete(self, taskid):
        popped = self.tracking.pop(taskid)
        self.heap.pop(self.heap.index(popped))
        heapq.heapify(self.heap)

REMOVED_KEY = MAX_PRIORITY_ID + 1

class TaskMaxHeapV4:

    def __init__(self):
        self.heap     = []
        self.tracking = {}

    def add(self, item):
        priority, task, user = item

        taskid     = MAX_TASK_ID - task
        priorityid = MAX_PRIORITY_ID - priority

        self.tracking[task] = [priorityid, taskid, user]

        heapq.heappush(
            self.heap
            , self.tracking[task]
        )

    def edit(self, taskid, new_priority):
        _, _, old_user = self.tracking[taskid]

        self.delete(taskid)
        self.add((new_priority, taskid, old_user))

    def pop(self):
        while self.heap:
            _, task, user = heapq.heappop(self.heap)

            if user != REMOVED_KEY:
                self.tracking.pop(MAX_TASK_ID - task)
                return user

        return -1

    def delete(self, taskid):
        deleted = self.tracking.pop(taskid)
        deleted[-1] = REMOVED_KEY


class TaskManager:

    def __init__(self, tasks: list[list[int]]):
        self.pq = TaskMaxHeapV4()
        self._parse_tasks(tasks)

    def add(self, userid: int, taskid: int, priority: int) -> None:
        self.pq.add((priority, taskid, userid))

    def get(self, taskid):
        return self.pq.get(taskid)

    def edit(self, taskid: int, new_priority: int) -> None:
        self.pq.edit(taskid, new_priority)

    def rmv(self, taskid: int) -> None:
        self.pq.delete(taskid)

    def execTop(self) -> int:
        return self.pq.pop()

    def _parse_tasks(self, tasks):
        for task in tasks:
            self.add(*task)

    def __repr__(self):
        return f"{json.dumps(self.pq.tracking, indent=4)}\n{'\n'.join(str(l) for l in self.pq.heap)}"


def executor(ids, args):
    results = []
    tm = TaskManager(args[0][0])

    print("EXECUTING")
    print(tm)

    for identifier, arg in zip(ids[1:], args[1:]):
        match identifier:
            case 'add':
                tm.add(*arg)
            case 'edit':
                tm.edit(*arg)
            case 'execTop':
                results.append(tm.execTop())
            case 'rmv':
                tm.rmv(*arg)

        print(identifier, arg)
        print(tm)
        print()

    return results, tm


test = [
    executor(
        ["TaskManager", "add", "edit", "execTop", "rmv", "add", "execTop"]
        , [[[[1, 101, 10], [2, 102, 20], [3, 103, 15]]], [4, 104, 5], [102, 8], [], [101], [5, 105, 15], []]
    )
    , executor(
        ["TaskManager","edit","execTop"]
        , [[[[8,17,33],[4,14,42]]],[14,21],[]]
    )
    , executor(
        ["TaskManager","edit","edit","execTop","execTop"]
        , [[[[4,15,16],[0,29,9],[10,17,50],[1,11,34],[10,12,16],[9,25,10],[10,10,26],[1,19,42]]],[19,27],[12,2],[],[]]
    )
]

"""
Sort stability: how do you get two tasks with equal priorities to be returned in the order they were originally added?

Tuple comparison breaks for (priority, task) pairs if the priorities are equal and the tasks do not have a default comparison order.

If the priority of a task changes, how do you move it to a new position in the heap?

Or if a pending task needs to be deleted, how do you find it and remove it from the queue?

#[prio, task, user] = deleted

        #if [prio, task, user] == self.heap[0]:
        #    heapq.heapreplace(self.heap, [REMOVED_KEY, task, user])
        #else:
"""
