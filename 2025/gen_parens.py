"""
Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

Example 1:

Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]

Example 2:

Input: n = 1
Output: ["()"]


["((()))","(()())","(())()","()(())","()()()"]
  111000   110100   110010   101100   101010

((()))
nest(nest(pair()))

1->1->0

(()())
nest(pair(), pair())

1->(0, 0)

(())()
nest(pair()), pair()
1->0, 0

()(())
pair(), nest(pair())
0, 1->0

()() (())
sequential
perfect inner

()()() (()()) (())() ()(()) ((()))
sequential
perfect inner with sequential

"""
def from_base_n(number_str, base):
    # Reverse the number string to process the least significant digit first
    number_str = number_str[::-1]

    result = 0
    for i, digit in enumerate(number_str):
        # Convert the character digit to its integer equivalent
        if digit.isdigit():
            digit_value = int(digit)
        else:
            # For base greater than 10 (e.g., for hexadecimal 'A' -> 10, 'B' -> 11, etc.)
            digit_value = ord(digit.upper()) - ord('A') + 10

        result += digit_value * (base ** i)

    return result

def to_base_n(number, base):
    if number == 0:
        return "0"  # Special case for 0

    digits = []
    while number:
        digits.append(int(number % base))
        number //= base

    # Reverse digits and convert to string
    return ''.join(str(digit) for digit in digits[::-1])


def binary_to_parens(digits):
    return ''.join(
        '(' if d == '1' else ')'
        for d in str(digits)
    )

def pair():
    return "()"

def nest(ops, i=1):
    return f"{'(' * i}{''.join(ops)}{')' * i}"

def nested(op=None, i=1):
    if i == 0:
        return ""

    if op is None:
        return nest([pair()], i - 1)

    return nest(op, i)

def pairs(i=1):
    if i == 0:
        return ""

    return ''.join(pair() for j in range(i))

def partial(i, j):
    return (
        pairs(i) + nested(j)
        , nested(i) + pairs(j)
        , pairs(j) + nested(i)
        , nested(j) + pairs(i)
    )


"""
10

1100 1
1010 2

111000 1, 2 0,1
110100 1, 3 0,2
110010 1, 4 0,3
101100 2, 3 1,2
101010 2, 4 1,3

11110000 0,1,2
11101000 0,1,3
11100100 0,1,4
11100010 0,1,5
11011000 0,2,3
11010100 0,2,4
11010010 0,2,5
11001100 0,3,4
11001010 0,3,5
10111000 1,2,3
10110100 1,2,4
10110010 1,2,5
10101100 1,3,4
10101010 1,3,5

    def create_generator(start, end):
        def inner():
            idx = start

            while idx < end - 1:
                for i in range(idx, end):
                    yield i

                yield None
                idx += 1

        return inner()

    for i, idx in enumerate(reversed(start_indexes)):
        generators.append(
            create_generator(idx, inner_count - (2 * i))
        )

"""
def replace(s):
    return s.replace('1', '(').replace('0', ')')

def gen_pairs(locs, length):
    built = ''.join([
        '1' if i in locs else '0'
        for i in range(length)
    ])

    return replace('1' + built + '0')

def gen_indexes(coords, max_values):
    pointers = [len(coords) - 2, len(coords) - 1]

    curr = list(coords)

    combs = []
    first_exhausted = False

    def create_generator(start, end, add1=False):
        def inner():
            for i in range(start + 1 if add1 else start, end + 1):
                yield i

        return inner()

    def exhaust_generator(base, gen, idx):
        tmp = []
        for i in gen[idx]:
            copy = list(base)
            copy[idx] = i
            tmp.append(copy)

        return tmp

    generators = [
        create_generator(start, end, add1 = i != len(coords) - 1)
        for i, (start, end) in enumerate(zip(coords, max_values))
    ]

    return generators

    def generate_new_coords(base, left):
        tmp = list(base)
        for i in range(left, len(base)):
            tmp[i] = tmp[i - 1] + 1
            generators[i] = create_generator(tmp[i], max_values[i])

        return tmp

    def rebuild_index(base):
        try:
            left, _ = pointers
            tmp = list(base)
            tmp[left] = next(generators[left])
            return generate_new_coords(tmp, left + 1)
        except StopIteration:
            if pointers[0] == 0:
                return None

            pointers[0] = pointers[0] - 1
            return rebuild_index(base)

    iters = 0

    #while not first_exhausted:
    while iters < 10:
        pointers[1] = len(coords) - 1

        combs.extend(
            exhaust_generator(curr, generators, pointers[1])
        )

        pointers[1] -= 1

        curr = rebuild_index(curr)

        print(curr, pointers)
        if curr is None:
            break

        iters += 1
        #first_exhausted = True

    return combs


def gen_indexes(coords, max_values):
    left  = len(coords) - 2

    curr = list(coords)
    combs = []

    while left >= 0:
        right = len(coords) - 1

        while right > left:
            for j in range(left, right):
                tmp_left = j

                while tmp_left < len(coords) - 1:
                    curr[tmp_left] = curr[tmp_left - 1] + 1
                    tmp_left += 1

                for i in range(curr[j], max_values[j] + 1):
                    curr[j] = i
                    combs.append(tuple(curr))

            right -= 1

        left -= 1
        curr[left] += 1

    return combs

def create_generator(start, end):
    def inner():
        for i in range(start, end):
            for j in range(i, end + 1):
                yield j

            yield None

    return inner()

def gen_indexes(coords, max_values):
    left  = len(coords) - 2
    right = len(coords) - 1

    curr        = [0] * len(coords)
    checkpoints = [
        [] for i in range(len(coords))
    ]

    combs = []

    generators = [
        list(create_generator(i, j))
        for i, j in zip(coords, max_values)
    ]

    len_generators = [len(gen) - 1 for gen in generators]
    iters = 0

    while left >= 0 and not all([
        current == gen
        for current, gen in zip(curr, len_generators)
    ]) and iters < 10:
        while generators[left][curr[left]] is not None:
            right = len(coords) - 1

            print(left, right, curr, checkpoints)

            while right > left:
                while generators[right][curr[right]] is not None:
                    combs.append([
                        generator[idx]
                        for idx, generator in zip(curr, generators)
                    ])
                    print(left, right, curr, combs[-1:])

                    curr[right] += 1

                if generators[right][curr[right]] is None:
                    if len(checkpoints[right]) + 1 != right + 1:
                        checkpoints[right].append(curr[right])

                    curr[right] += 1

                if curr[right] >= len(generators[right]):
                    curr[right] = checkpoints[right]

                right -= 1

            curr[left] += 1

        if generators[left][curr[left]] is None:
            if len(checkpoints[left]) + 1 != left + 1:
                checkpoints[left].append(curr[left])

            curr[left] += 1

        left -= 1
        iters += 1

    return combs

def gen_indexes(coords, max_values):
    left  = len(coords) - 2

    curr = list(coords)

    combs = []

    while left >= 0:
        right = len(coords) - 1

        while right > left:
            for i in range(right + 1, len(coords)):
                curr[i] = curr[i - 1] + 1

            print(curr)

            while curr[right] < max_values[right]:
                for i in range(curr[-1], max_values[-1] + 1):
                    curr[-1] = i
                    combs.append(tuple(curr))

                curr[right] += 1

                for i in range(right + 1, len(coords)):
                    curr[i] = curr[i - 1] + 1

                print(left, right, curr)

            right -= 1

        left -= 1

    return combs

def gen_indexes(coords, max_values):
    left  = len(coords) - 2
    right = len(coords) - 1

    curr = list(coords)

    combs = []

    while left >= 0:
        while curr[right] < max_values[right]:
            right = len(coords) - 1
            while right > left:
                for i in range(curr[-1], max_values[-1] + 1):
                    curr[-1] = i
                    combs.append(tuple(curr))

                right -= 1

                curr[right] = min(
                    curr[right] + 1
                    , max_values[right]
                )

                for i in range(right + 1, len(coords)):
                    curr[i] = curr[i - 1] + 1

                print(left, right, curr)

        right -= 1
        left -= 1

        curr[right] = min(
            curr[right] + 1
            , max_values[right]
        )

        for i in range(right + 1, len(coords)):
            curr[i] = curr[i - 1] + 1

        print(curr)

    return combs

def indexes_to_parens(ind):
    maxlen = len(ind) * 2
    return '(' + ''.join(['(' if idx in ind else ')' for idx in range(maxlen)]) + ')'

def gen_product(coords, max_values):
    left  = len(coords) - 2
    right = len(coords) - 1

    curr = list(coords)

    combs = []

    def is_exhausted(start_idxs, stop_idxs):
        return all([
            start >= stop
            for start, stop in zip(start_idxs, stop_idxs)
        ])

    while not is_exhausted(curr, max_values):
        while curr[left] <= max_values[left]:
            right = len(coords) - 1

            tmp_left = left + 1
            while tmp_left <= right:
                curr[tmp_left] = curr[tmp_left - 1] + 1
                tmp_left += 1

            while curr[right] <= max_values[right]:
                print(left, right, curr)
                combs.append(tuple(curr))
                curr[right] += 1

            curr[left] += 1
            print(left, right, curr, 'hoi')

        if left == 0:
            curr[0] -= 1
            left = len(coords) - 2
        else:
            left -= 1

        curr[left] += 1
        curr[left + 1] = curr[left] + 1

    return combs

def gen_tokens(top, bottom, num_pairs):
    if top == bottom:
        return replace('10')

    inner_count = len(top) - 2

    tokens = []

    start_indexes = list(range(num_pairs - 1))
    boundaries = []

    curr_idx = len(start_indexes) - 2

    final_indexes = list(range(1, inner_count, 2))

    print(start_indexes, final_indexes)

    def is_exhausted(start_idxs, stop_idxs):
        return all([
            start >= stop
            for start, stop in zip(start_idxs, stop_idxs)
        ])

    while (
        curr_idx >= 0
            and not is_exhausted(start_indexes, final_indexes)
    ):
        while start_indexes[-1] <= final_indexes[-1]:
            boundaries.append(tuple(start_indexes))
            start_indexes[-1] += 1

        if start_indexes[curr_idx] >= final_indexes[curr_idx]:
            curr_idx -= 1

        start_indexes[curr_idx] += 1
        start_indexes[curr_idx + 1:] = [
            start_indexes[curr_idx] + i
            for i in range(1, num_pairs - curr_idx - 1)
        ]

        print(start_indexes, curr_idx)

    print(boundaries)

    return [
        gen_pairs(b, inner_count)
        for b in boundaries
    ]

def gen_indexes(coords, max_values):
    left  = len(coords) - 2
    right = len(coords) - 1

    curr = list(coords)

    combs = []

    while left >= -1:
        while right > left:
            right = len(coords) - 1
            for i in range(curr[-1], max_values[-1] + 1):
                curr[-1] = i
                combs.append(tuple(curr))

            while curr[right] == max_values[right] and right > left:
                right -= 1

            curr[right] += 1

            for i in range(right + 1, len(coords)):
                curr[i] = curr[i - 1] + 1

        left -= 1

    return combs

def gen_parens(n):
    top = "1" * n + "0" * n
    bottom = "10" * n

    if top == bottom:
        return '()'

    inner_count = n * 2 - 2

    start = list(range(n - 1))
    final = list(range(1, inner_count, 2))

    return [
        indexes_to_parens(idx)
        for idx in gen_indexes(start, final)
    ]

test = [
    gen_parens(1)
    , gen_parens(2)
    , gen_parens(3)
    , gen_parens(4)
    , gen_parens(5)
]
