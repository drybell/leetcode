"""
Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example 1:

Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]

Explanation:
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.

The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

Example 2:

Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:

Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.

Naive:

I guess this is triple pointer?

[-1,0,1,2,-1,-4]
  ^ ^ ^
-1 + 0 + 1 = 0
push [-1, 0, 1]

[-1,0,1,2,-1,-4]
  ^ ^ ^
next up is 2
2 is larger than i, j, k
move largest to 2

[-1,0,1,2,-1,-4]
  ^ ^   ^
-1 + 0 + 2 = 1
1 > 0 so move largest

[-1,0,1,2,-1,-4]
  ^ ^      ^
-1 + 0 + -1 = 0 push

[-1,0,1,2,-1,-4]
  ^ ^      ^
next up is either 2 or -4
2 > 0 so move largest
[-1,0,1,2,-1,-4]
  ^   ^    ^

-4 < 0 so move smallest
[-1,0,1,2,-1,-4]
  ^ ^         ^

[-1,0,1,2,-1,-4]
  ^   ^    ^
-1 + 1 + -1 = -1
-1 < 0 so move smallest

[-1,0,1,2,-1,-4]
    ^ ^    ^
0 + 1 + -1 = 0 push





[-1,0,1,2,-1,-4]
  ^   ^ ^
-1 + 1 + 2 != 0

[-1,0,1,2,-1,-4]
  ^     ^  ^
push [-1, 2, -1]

[-1,0,1,2,-1,-4]
    ^ ^ ^
0 + 1 + 2 != 0

[-1,0,1,2,-1,-4]
    ^ ^    ^
0 + 1 + -1 = 0
push [0, 1, -1]

[-1,0,1,2,-1,-4]
      ^ ^  ^
1 + 2 - 1 != 0

[-1,0,1,2,-1,-4]
      ^ ^     ^


threesum means two things
a number, its inverse, and 0 exist
a number, and two numbers < 0 that add up to it exist

find inverse and 0
[-1,0,1,2,-1,-4]
  ^ ^ ^

find value and two that add up
[-1,0,1,2,-1,-4]
  ^     ^  ^



"""

def three_sum(nums):
    pointers  = [0, 1, 2]
    traversed = []

    sums = []

    def eval_sum(*args):
        return sum(args)

    def get_next_idx(index, traverse_index=None):
        for idx in range(0, len(nums)):
            if index + idx == len(nums):
                index = 0 - idx

            if (
                index + idx not in pointers
            ):
                if traverse_index is not None:
                    if (
                        index + idx not in [
                            t[traverse_index]
                            for t in traversed
                        ]
                    ):
                        return index + idx
                else:
                    return index + idx

    def get_largest(iy, jy, ky):
        if ky >= jy >= iy or ky >= iy >= jy:
            return 2
        elif jy >= ky >= iy or jy >= iy >= ky:
            return 1
        else:
            return 0

    def get_smallest(iy, jy, ky):
        if ky >= jy >= iy or jy >= ky >= iy:
            return 0
        elif jy >= iy >= ky or iy >= jy >= ky:
            return 2
        else:
            return 1

    def move_largest(iy, jy, ky):
        if ky >= jy >= iy or ky >= iy >= jy:
            pointers[-1] = get_next_idx(pointers[-1], 2)
        elif jy >= ky >= iy or jy >= iy >= ky:
            pointers[1] = get_next_idx(pointers[1], 1)
        else:
            pointers[0] = get_next_idx(pointers[0], 0)

    def move_smallest(iy, jy, ky):
        if ky >= jy >= iy or jy >= ky >= iy:
            pointers[0] = get_next_idx(pointers[0], 0)
        elif jy >= iy >= ky or iy >= jy >= ky:
            pointers[-1] = get_next_idx(pointers[-1], 2)
        else:
            pointers[1] = get_next_idx(pointers[1], 1)

    TERMINATOR = 100
    iters = 0

    while (
        all(map(lambda x: x < len(nums), pointers))
        and iters < TERMINATOR
    ):
        traversed.append(pointers)

        iy, jy, ky = [nums[idx] for idx in pointers]

        total = eval_sum(iy, jy, ky)

        if total > 0:
            #print("MOVING LARGEST")
            move_largest(iy, jy, ky)
        elif total == 0:
            if [iy, jy, ky] not in sums:
                sums.append([iy, jy, ky])

            # Look at best possible options
            next_idx = get_next_idx(max(pointers))

            if nums[next_idx] >= 0:
                idx = get_largest(iy, jy, ky)
            else:
                idx = get_smallest(iy, jy, ky)

            #print(f"EQUALLED 0, MOVING {idx} {pointers[idx]} -> {next_idx}")
            pointers[idx] = next_idx
        else:
            #print("MOVING SMALLEST")
            move_smallest(iy, jy, ky)

        #print(pointers)
        iters += 1

    #print()

    return sums, traversed


def three_sum(nums):
    pointers = [0, 1, 2]
    traversed = []
    sums = []

    TERMINATOR = 100
    iters = 0

    def in_traversed(ix, jx, kx):
        sortedp = sorted([ix, jx, kx])
        return (sortedp in traversed, sortedp)

    def add_to_traversed(ix, jx, kx):
        res, sortedp = in_traversed(ix, jx, kx)
        if not res:
            traversed.append(sortedp)

    def eval_sum(*args):
        return sum(args)

    def find_largest(iy, jy, ky):
        if iy >= jy >= ky or iy >= ky >= jy:
            return 0
        elif jy >= iy >= ky or jy >= ky >= iy:
            return 1
        else:
            return 2

    def find_smallest(iy, jy, ky):
        if iy >= jy >= ky or jy >= iy >= ky:
            return 2
        elif jy >= ky >= iy or ky >= jy >= iy:
            return 0
        else:
            return 1

    def clone(index, new_value):
        new_pointers = [i for i in pointers]
        new_pointers[index] = new_value
        return new_pointers

    def move_to_next_index(index, return_only=False):
        for i in range(0, len(nums)):
            new_pos = clone(index, i)
            if not in_traversed(*new_pos)[0] and len(set(new_pos)) == 3:
                if return_only:
                    return i

                return new_pos

    def arg_closest_to_zero(vals):
        arg = vals[0]
        idx = None

        for i, val in enumerate(vals[1:]):
            if abs(val) < abs(arg):
                arg = val
                idx = i

        return idx

    def find_next_index():
        """
        find the index with the closest to 0 sum
        """
        new_pos = []
        new_sums  = []

        for i, index in enumerate(pointers):
            new_idx = move_to_next_index(i, return_only=True)
            cloned = clone(i, new_idx)
            new_pos.append(cloned)
            new_sums.append(sum(cloned))

        return new_pos[arg_closest_to_zero(new_sums)]

    while (
        all(map(lambda x: x < len(nums), pointers))
        and iters < TERMINATOR
    ):
        add_to_traversed(*pointers)

        iy, jy, ky = [nums[idx] for idx in pointers]

        total = eval_sum(iy, jy, ky)

        #print(f"TOTAL == {total} {[(x, y) for x, y in zip(pointers, [iy, jy, ky])]}")

        if total == 0:
            if (sorted_pointers := sorted(pointers)) not in sums:
                sums.append(sorted_pointers)

        pointers = find_next_index()
        #print(pointers)

        if pointers is None:
            return [[
                nums[i]
                for i in sublist
            ] for sublist in sums], traversed

        iters += 1

    return [[
        nums[i]
        for i in sublist
    ] for sublist in sums], traversed


def three_sum(nums):
    sums = []

    #print(f"\n\n{nums}\n\n")

    def find_inverse_and_zero(x, y):
        found_0       = -1
        found_inverse = -1

        for ix, iy in enumerate(nums):
            if ix == x:
                continue

            if found_0 == -1:
                if iy == 0 and ix != found_inverse:
                    found_0 = ix
            if found_inverse == -1:
                if y == (iy * -1) and ix != found_0:
                    found_inverse = ix

            #print(f"\t[{ix} ^ {x}] {iy} == {y} FOUND 0: {found_0} FOUND INVERSE: {found_inverse}")

            if found_0 != -1 and found_inverse != -1:
                return sorted([
                    x, found_0, found_inverse
                ])

        return None

    def find_value(x1, y1, x2, y2):
        for ix, iy in enumerate(nums):
            if ix in [x1, x2]:
                continue

            #print(f"\t{iy} + {y1} = {y2}")
            if iy + y1 == -1 * y2:
                return ix

    def find_pairs_adding_up_to(x, y):
        pairs = []

        for ix, iy in enumerate(nums):
            if ix == x:
                continue

            found_pair = find_value(
                ix, iy, x, y
            )

            if found_pair is not None:
                pairs.append(sorted([
                    x, ix, found_pair
                ]))

        return pairs

    for x, y in enumerate(nums):
        #print()
        results = [
            find_inverse_and_zero(x, y)
            , *find_pairs_adding_up_to(x, y)
        ]

        #print(results)

        for result in results:
            if result is None:
                continue

            if (ys := sorted([nums[i] for i in result])) not in sums:
                sums.append(ys)

    return sums


def three_sum(nums):
    sums = []

    sorted_nums = sorted(nums)

    for i in range(len(nums)):
        if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
            continue

        j, k = (i + 1, len(nums) - 1)

        while (j < k):
            iy, jy, ky = [sorted_nums[idx] for idx in [i, j, k]]

            if (total := sum([iy, jy, ky])) == 0:
                sums.append([iy, jy, ky])

                while (j < k and sorted_nums[j] == sorted_nums[j + 1]):
                    j += 1
                while (k > j and sorted_nums[k] == sorted_nums[k - 1]):
                    k -= 1

                j += 1
                k -= 1
            elif total > 0:
                k -= 1
            else:
                j += 1

    return sums

test = [
    three_sum([-1,0,1,2,-1,-4])
    , three_sum([-10,8,-2,2,1,18,-12,-5,10,0])
    , three_sum([-1, 0, 1, 0])
    , three_sum([-1,0,1,2,-1,-4,-2,-3,3,0,4])
]

"""

Notes:
finally figured out trick, problem is its too slow :(
instead, it is really just two pointers, but instead you sort the array first

[-1, 0, 1, 2, -1, 4]
sort
[-1, -1, 0, 1, 2, 4]
  ^   ^           ^
  i   j           k

lock i, then increment j if total < 0 and decrement k if total > 0



        elif total > 0:
            #print(f"TOTAL > 0 {[(x, y) for x, y in zip(pointers, [iy, jy, ky])]}")
            pointeridx = find_largest(iy, jy, ky)
            pointers = move_to_next_index(pointeridx)
        else:
            #print(f"TOTAL < 0 {[(x, y) for x, y in zip(pointers, [iy, jy, ky])]}")
            pointeridx = find_smallest(iy, jy, ky)
            pointers = move_to_next_index(pointeridx)



        if ky >= jy >= iy:
            k = get_next_idx(k)
            j = get_next_idx(j)
        elif ky >= iy >= jy:
            k = get_next_idx(k)
            i = get_next_idx(i)
        elif jy >= ky >= iy:
            k = get_next_idx(k)
            j = get_next_idx(j)
        elif jy >= iy >= ky:
            j = get_next_idx(j)
            i = get_next_idx(i)
        elif iy >= ky >= jy:
            k = get_next_idx(k)
            i = get_next_idx(i)
        else:
            j = get_next_idx(j)
            i = get_next_idx(i)



        if ky >= jy >= iy:
            k = get_next_idx(k)
        elif ky >= iy >= jy:
            k = get_next_idx(k)
            i = get_next_idx(i)
        elif jy >= ky >= iy:
            j = get_next_idx(j)
        elif jy >= iy >= ky:
            j = get_next_idx(j)
            i = get_next_idx(i)
        elif iy >= ky >= jy:
            i = get_next_idx(i)
        else:
            i = get_next_idx(i)
            j = get_next_idx(j)


"""
