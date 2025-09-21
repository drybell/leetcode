"""
3508. Implement Router
https://leetcode.com/problems/implement-router/description/?envType=daily-question&envId=2025-09-20

Design a data structure that can efficiently manage data packets in a network router. Each data packet consists of the following attributes:

source: A unique identifier for the machine that generated the packet.
destination: A unique identifier for the target machine.
timestamp: The time at which the packet arrived at the router.
Implement the Router class:

Router(int memoryLimit): Initializes the Router object with a fixed memory limit.

memoryLimit is the maximum number of packets the router can store at any given time.
If adding a new packet would exceed this limit, the oldest packet must be removed to free up space.
bool addPacket(int source, int destination, int timestamp): Adds a packet with the given attributes to the router.

A packet is considered a duplicate if another packet with the same source, destination, and timestamp already exists in the router.
Return true if the packet is successfully added (i.e., it is not a duplicate); otherwise return false.
int[] forwardPacket(): Forwards the next packet in FIFO (First In First Out) order.

Remove the packet from storage.
Return the packet as an array [source, destination, timestamp].
If there are no packets to forward, return an empty array.
int getCount(int destination, int startTime, int endTime):

Returns the number of packets currently stored in the router (i.e., not yet forwarded) that have the specified destination and have timestamps in the inclusive range [startTime, endTime].
Note that queries for addPacket will be made in increasing order of timestamp.

Example 1:

Input:
["Router", "addPacket", "addPacket", "addPacket", "addPacket", "addPacket", "forwardPacket", "addPacket", "getCount"]
[[3], [1, 4, 90], [2, 5, 90], [1, 4, 90], [3, 5, 95], [4, 5, 105], [], [5, 2, 110], [5, 100, 110]]

Output:
[null, true, true, false, true, true, [2, 5, 90], true, 1]

Explanation

Router router = new Router(3); // Initialize Router with memoryLimit of 3.
router.addPacket(1, 4, 90); // Packet is added. Return True.
router.addPacket(2, 5, 90); // Packet is added. Return True.
router.addPacket(1, 4, 90); // This is a duplicate packet. Return False.
router.addPacket(3, 5, 95); // Packet is added. Return True
router.addPacket(4, 5, 105); // Packet is added, [1, 4, 90] is removed as number of packets exceeds memoryLimit. Return True.
router.forwardPacket(); // Return [2, 5, 90] and remove it from router.
router.addPacket(5, 2, 110); // Packet is added. Return True.
router.getCount(5, 100, 110); // The only packet with destination 5 and timestamp in the inclusive range [100, 110] is [4, 5, 105]. Return 1.

Example 2:

Input:
["Router", "addPacket", "forwardPacket", "forwardPacket"]
[[2], [7, 4, 90], [], []]

Output:
[null, true, [7, 4, 90], []]

Explanation

Router router = new Router(2); // Initialize Router with memoryLimit of 2.
router.addPacket(7, 4, 90); // Return True.
router.forwardPacket(); // Return [7, 4, 90].
router.forwardPacket(); // There are no packets left, return [].

Constraints:

2 <= memoryLimit <= 105
1 <= source, destination <= 2 * 105
1 <= timestamp <= 109
1 <= startTime <= endTime <= 109
At most 105 calls will be made to addPacket, forwardPacket, and getCount methods altogether.
queries for addPacket will be made in increasing order of timestamp.


Strategy:

looks like we're going to use a FIFO queue to store the packets,
as the oldest needs to be removed

First solution got a TLE, using a deque and a dict to track destination counts
I might try just using the deque and utilizing constant append/pop to find the counts

This approach also resulted in TLE. I'll have to figure out
an efficient way to store time boundaries so we can count quickly

Trying a minheap also results in TLE as we spend too long
rebuilding the heap after popping
"""

from utils import executor

from queue import deque
import bisect

class ManagerV1:
    def __init__(self, limit):
        self.q      = deque([], limit)
        self.counts = {}

    def pop(self):
        psrc, pdest, pts = self.q.popleft()
        self.counts[pdest].pop(
            bisect.bisect(
                self.counts[pdest]
                , pts
            ) - 1
        )

        return [psrc, pdest, pts]

    def add(self, source, dest, ts):
        newpacket = [source, dest, ts]
        if newpacket in self.q:
            return False

        if len(self.q) == self.q.maxlen:
            self.pop()

        self.q.append(newpacket)
        if dest in self.counts:
            bisect.insort(self.counts[dest], ts)
        else:
            self.counts[dest] = [ts]

        return True

    def forward(self):
        if not self.q:
            return []

        return self.pop()

    def count(self, dest, start, end):
        if not self.counts[dest]:
            return 0
        if self.counts[dest][-1] < start or self.counts[dest][0] > end:
            return 0

        left = bisect.bisect_left(
            self.counts[dest]
            , start
        ) - 1

        right = bisect.bisect(
            self.counts[dest]
            , end
        ) - 1

        if left == right:
            if self.counts[dest][0] < start and self.counts[dest][-1] > end:
                return 0
            else:
                return 1

        return right - left

class ManagerV2:
    def __init__(self, limit):
        self.q = deque([], limit)
        self.dests = {}

    def pop(self):
        psrc, pdest, pts = self.q.popleft()
        if self.dests[pdest] == 1:
            self.dests.pop(pdest)
        else:
            self.dests[pdest] -= 1
        return [psrc, pdest, pts]

    def add(self, source, dest, ts):
        newpacket = [source, dest, ts]
        if newpacket in self.q:
            return False

        if len(self.q) == self.q.maxlen:
            self.pop()

        self.q.append(newpacket)
        if self.dests.get(dest) is not None:
            self.dests[dest] += 1
        else:
            self.dests[dest] = 1

        return True

    def forward(self):
        if not self.q:
            return []

        return self.pop()

    def count(self, dest, start, end):
        if not self.dests.get(dest):
            return 0

        cloned = self.q.copy()
        ctr = 0
        while cloned:
            _, pdest, ts = cloned.popleft()
            if pdest != dest:
                continue
            else:
                if start <= ts <= end:
                    ctr += 1

        return ctr

import heapq

GARBAGE_TS = 10**9 + 1
MAX_SOURCE = (2 * 10**5) + 1

class ManagerV3:
    def __init__(self, limit):
        self.q = deque([], limit)
        self.size = 0

        self.counts = {}

    def pop_from_heap(self, psrc, pdst, pts):
        cache = []
        while self.counts[pdst]:
            popped = heapq.heappop(self.counts[pdst])
            if popped == [pts, psrc]:
                break
            else:
                cache.insert(0, popped)

        while cache:
            heapq.heappush(self.counts[pdst], cache.pop(0))

    def add_to_heap(self, src, dst, ts):
        if self.counts.get(dst) is None:
            self.counts[dst] = [[ts, src]]
        else:
            heapq.heappush(self.counts[dst], [ts, src])

    def pop(self):
        self.size -= 1
        popped = self.q.popleft()

        self.pop_from_heap(*popped)
        return popped

    def add(self, source, dest, ts):
        newpacket = [source, dest, ts]
        if newpacket in self.q:
            return False

        if self.size == self.q.maxlen:
            self.pop()

        self.q.append(newpacket)
        self.size += 1

        self.add_to_heap(*newpacket)

        return True

    def forward(self):
        if not self.q:
            return []

        return self.pop()

    def count(self, dest, start, end):
        if self.counts.get(dest) is None:
            return 0

        ctr = 0

        cloned = list(self.counts[dest])
        while cloned:
            [ts, src] = heapq.heappop(cloned)

            if ts < start:
                continue
            if start <= ts <= end:
                ctr += 1
            if ts > end:
                break

        return ctr

class Manager:
    def __init__(self, limit):
        self.q = deque([], limit)
        self.size = 0

        self.counts = {}
        self.dests  = {}

    def add_to_dest(self, src, dst, ts):
        if self.counts.get(dst) is not None:
            self.counts[dst][(ts, src)] = 1
        else:
            self.counts[dst] = {(ts, src): 1}

        if self.dests.get(dst) is not None:
            self.dests[dst].append(ts)
        else:
            self.dests[dst] = deque([ts])

    def pop_from_dest(self, src, dst, ts):
        self.counts[dst].pop((ts, src), None)
        self.dests[dst].popleft()

    def pop(self):
        self.size -= 1
        popped = self.q.popleft()

        self.pop_from_dest(*popped)
        return popped

    def add(self, source, dest, ts):
        newpacket = [source, dest, ts]

        if self.counts.get(dest, {}).get((ts, source)) is not None:
            return False

        if self.size == self.q.maxlen:
            self.pop()

        self.q.append(newpacket)
        self.size += 1

        self.add_to_dest(*newpacket)

        return True

    def forward(self):
        if not self.q:
            return []

        return self.pop()

    def count(self, dest, start, end):
        data = self.dests.get(dest)
        if data is None:
            return 0

        return (
            bisect.bisect_right(data, end)
            - bisect.bisect_left(data, start)
        )
        #return len([
        #    t for _, t in data.keys()
        #    if start <= t <= end
        #])

class Router:

    def __init__(self, memoryLimit: int):
        self.inner = Manager(memoryLimit)

    def addPacket(self, source: int, destination: int, timestamp: int) -> bool:
        return self.inner.add(source, destination, timestamp)

    def forwardPacket(self) -> list[int]:
        return self.inner.forward()

    def getCount(self, destination: int, startTime: int, endTime: int) -> int:
        return self.inner.count(destination, startTime, endTime)


    def __repr__(self):
        # \t{self.inner.dests}\n
        return f'Router(\n\t{self.inner.q},\n)\n'

test = [
    # [True, [7, 4, 90], []]
    executor(
        Router
        , ["Router", "addPacket", "forwardPacket", "forwardPacket"]
        , [[2], [7, 4, 90], [], []]
    )
    # [True, True, False, True, True, [2, 5, 90], True, 1]
    , executor(
        Router
        , ["Router", "addPacket", "addPacket", "addPacket", "addPacket", "addPacket", "forwardPacket", "addPacket", "getCount"]
        , [[3], [1, 4, 90], [2, 5, 90], [1, 4, 90], [3, 5, 95], [4, 5, 105], [], [5, 2, 110], [5, 100, 110]]
    )
    # [True, 1]
    , executor(
        Router
        , ["Router","addPacket","getCount"]
        , [[4],[4,5,1],[5,1,1]]
    )
    # [True, True, False, True, True, [2, 5, 90], True, 1]
    , executor(
        Router
        , ["Router","addPacket","addPacket","addPacket","addPacket","addPacket","forwardPacket","addPacket","getCount"]
        , [[3],[1,4,90],[2,5,90],[1,4,90],[3,5,95],[4,5,105],[],[5,2,110],[5,100,110]]
    )
    # [True, True, 2]
    , executor(
        Router
        , ["Router","addPacket","addPacket","getCount"]
        , [[4],[4,2,1],[3,2,1],[2,1,1]]
    )
    # [True, True, False, 2, [1, 4, 1], 1]
    , executor(
        Router
        , ["Router","addPacket","addPacket","addPacket","getCount","forwardPacket","getCount"]
        , [[2],[1,4,1],[5,4,1],[1,4,1],[4,1,1],[],[4,1,1]]
    )
    # [True, True, True, True, [4, 3, 1], True, 0]
    , executor(
        Router
        , ["Router","addPacket","addPacket","addPacket","addPacket","forwardPacket","addPacket","getCount"]
        , [[5],[4,3,1],[4,1,1],[2,4,1],[3,2,1],[],[2,4,6],[4,4,5]]
    )
    # [null,true,true,true,0,1,true,[2,3,1],false]
    , executor(
        Router
        , ["Router","addPacket","addPacket","addPacket","getCount","getCount","addPacket","forwardPacket","addPacket"]
        , [[5],[2,3,1],[5,2,5],[2,3,5],[3,4,4],[3,5,5],[3,2,5],[],[2,3,5]]
    )
    , executor(
        Router
        , ["Router","addPacket","getCount","addPacket","addPacket","getCount","addPacket","addPacket","getCount","addPacket","forwardPacket","addPacket","getCount","addPacket","forwardPacket","addPacket","addPacket","getCount","getCount","getCount","getCount","getCount","getCount","addPacket","addPacket","getCount","addPacket","addPacket","addPacket","forwardPacket","addPacket","forwardPacket","getCount","addPacket","addPacket","forwardPacket","addPacket","addPacket","addPacket","getCount","forwardPacket","getCount","forwardPacket","forwardPacket","getCount","addPacket","addPacket","getCount","getCount","forwardPacket","addPacket","getCount","addPacket","forwardPacket","getCount","addPacket","addPacket","addPacket","addPacket","forwardPacket","getCount","addPacket","addPacket","getCount","getCount","forwardPacket","forwardPacket","forwardPacket","getCount","addPacket","addPacket","addPacket","getCount","forwardPacket","addPacket","addPacket","getCount","addPacket","forwardPacket","forwardPacket","addPacket","getCount","addPacket","addPacket","addPacket","forwardPacket","addPacket","getCount","getCount","addPacket","forwardPacket","forwardPacket","forwardPacket","forwardPacket","addPacket","addPacket","forwardPacket","getCount","getCount","addPacket"]
        , [[49],[4,1,1],[1,1,1],[2,3,1],[3,1,2],[1,1,1],[1,4,2],[2,4,2],[3,2,2],[2,1,2],[],[2,3,2],[3,1,1],[4,5,2],[],[1,4,2],[3,2,7],[1,7,7],[4,3,7],[5,1,1],[1,5,6],[3,6,7],[3,4,4],[3,4,11],[2,5,11],[5,6,9],[1,3,14],[2,4,14],[3,2,16],[],[2,1,16],[],[5,8,8],[3,2,16],[1,2,16],[],[4,2,16],[2,4,16],[2,3,16],[3,10,12],[],[5,11,13],[],[],[5,7,13],[1,4,16],[4,5,16],[1,5,8],[5,15,15],[],[5,3,16],[3,16,16],[5,4,16],[],[1,5,15],[2,1,20],[2,5,20],[5,4,20],[2,3,23],[],[2,10,17],[1,5,23],[5,4,23],[1,16,18],[4,9,22],[],[],[],[4,1,15],[2,3,23],[1,4,24],[2,5,24],[4,3,17],[],[2,1,28],[4,1,28],[2,6,18],[1,2,28],[],[],[2,3,33],[2,22,26],[5,3,33],[4,5,33],[5,4,33],[],[5,1,33],[1,30,31],[5,13,16],[2,5,34],[],[],[],[],[3,2,38],[3,4,38],[],[3,5,13],[1,36,38],[3,4,38]]
    )
]
