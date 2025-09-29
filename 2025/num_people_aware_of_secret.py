"""
2327. Number of People Aware of a Secret
https://leetcode.com/problems/number-of-people-aware-of-a-secret/description

On day 1, one person discovers a secret.

You are given an integer delay, which means that each person will share the secret with a new person every day, starting from delay days after discovering the secret. You are also given an integer forget, which means that each person will forget the secret forget days after discovering it. A person cannot share the secret on the same day they forgot it, or on any day afterwards.

Given an integer n, return the number of people who know the secret at the end of day n. Since the answer may be very large, return it modulo 109 + 7.

Example 1:

Input: n = 6, delay = 2, forget = 4
Output: 5

Explanation:

Day 1: Suppose the first person is named A. (1 person)
Day 2: A is the only person who knows the secret. (1 person)
Day 3: A shares the secret with a new person, B. (2 people)
Day 4: A shares the secret with a new person, C. (3 people)
Day 5: A forgets the secret, and B shares the secret with a new person, D. (3 people)
Day 6: B shares the secret with E, and C shares the secret with F. (5 people)

Example 2:

Input: n = 4, delay = 1, forget = 3
Output: 6

Explanation:

Day 1: The first person is named A. (1 person)
Day 2: A shares the secret with B. (2 people)
Day 3: A and B share the secret with 2 new people, C and D. (4 people)
Day 4: A forgets the secret. B, C, and D share the secret with 3 new people. (6 people)

Constraints:

2 <= n <= 1000
1 <= delay < forget <= n


Strategy:

n = 6, delay = 2, forget = 4

[0, 1, 2, 3, 4, 5]
       ^  ^  ^  ^
       A shares B
          |  |  |
          A shares C
             A forget
             B shares D
                B shares E
                C shares F

base case -> always start with 1
this means every delay idx we increase count by delay
every forget + 1 days we lose a sharing person

i'm going to start with a deque as the naive implementation
just to get a feel for the current amount of aware people
during a particular day along with what to keep track of
during day iteration

Obviously the initial approach TLE's, but we identified
the mechanism to track the aware and able to share people

"""

from collections import deque

MODULUS = 10**9 + 7

class AwareQueueV1:
    """
    Maybe instead of holding every single person,
    we hold the count of how many people were added on the
    particular day?
    """
    def __init__(self, delay, forget):
        self.q = deque([delay - 1])
        self.delay = delay
        self.forget = forget
        self.size = 1

    def tick(self, day):
        print(f"DAY {day}")

        while self.q[0] + 1 == self.forget:
            forgot = self.q.popleft()
            print(f"{forgot} FORGOT")
            self.size -= 1

        for i in range(self.size):
            self.q[i] += 1

            if self.q[i] >= self.delay:
                print(f"{self.q[i]} adds new")
                self.q.append(0)
                self.size += 1

        print(self.size, self.q)

def people_awarev1(n, delay, forget):
    #print()
    if forget < delay:
        return 0

    aware = AwareQueueV1(delay, forget)

    for day in range(delay, n):
        aware.tick(day)

    return aware.size % MODULUS

class AwareQueue:
    def __init__(self, delay, forget):
        self.q = deque([[1, delay - 1]])

        self.delay = delay
        self.forget = forget
        self.size = 1

    def tick(self, day):
        while self.q[0][1] + 1 == self.forget:
            forgot = self.q.popleft()
            self.size -= 1

        toadd = 0

        for i in range(self.size):
            self.q[i][1] += 1
            if self.q[i][1] >= self.delay:
                toadd += self.q[i][0]

        self.q.append([toadd, 0])
        self.size += 1

    def aware(self):
        return sum(
            s[0] for s in self.q
        )

def people_aware(n, delay, forget):
    if forget < delay:
        return 0

    aware = AwareQueue(delay, forget)

    for day in range(delay, n):
        aware.tick(day)

    return aware.aware() % MODULUS



test = [
    people_aware(6, 2, 4)
    , people_aware(4, 1, 3)
    , people_aware(6, 1, 2)
]

"""
GRAVEYARD

def people_awarev1(n, delay, forget):
    if forget < delay:
        return 0

    print()
    print(n, delay, forget)
    aware = 1
    able_to_share = 1
    delayed = 0

    i = 0
    while i < n:
        for j in range(delay, forget):
            aware += able_to_share
            delayed += 1
            print('inner', j, aware, able_to_share)

        aware -= 1
        i += j
        print(i, aware, able_to_share)

    return aware

def people_aware(n, delay, forget):
    #print()
    if forget <= delay:
        return 0

    aware = 1
    able_to_share = 1
    delayed = 0

    gap = forget - delay
    q = [1] * gap
    forgot = [0, 1]

    for day in range(delay, n):
        if forgot[0]:
            new = sum(forgot)
            forgot[0] = forgot[1]
            forgot[1] = new
        if day == forget:
            forgot[0] = 1

        q[0] = day - forgot[0]

        print(f"pop time {day} {gap} {forgot}")
        for i in range(1, len(q)):
            q[i] = q[i - 1] * 2

        print(q)

    return q[-1] % MODULUS



"""
