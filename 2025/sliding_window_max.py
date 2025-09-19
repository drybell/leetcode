"""
239. Sliding Window Maximum
https://leetcode.com/problems/sliding-window-maximum/description/

You are given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.

Return the max sliding window.

Example 1:

Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]
Explanation:
Window position                Max
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7

Example 2:

Input: nums = [1], k = 1
Output: [1]

Constraints:

1 <= nums.length <= 10^5
-10^4 <= nums[i] <= 10^4
1 <= k <= nums.length

Notes:
Initial Solution caused TLE. Makes sense since I thought this
problem was pretty easy from the onset, so was wondering what the
trick would be.

Looks like we'll probably have to do a two-pointer approach, where
we skip over sliding the window and instead re-use the same max
value until the new pointer value is greater than the last

 1  3  -1  -3  5  3  6  7
 ^      ^
 max = 3

 1  3  -1  -3  5  3  6  7
 ^             ^
 nums[right] > maxes[-1] -> 5

this approach won't work since when the current max
gets ejected out of the sliding window we will have to
recalculate the max


 1  3  -1  -2  0  4 -3  5  3  6  7
 ^  ^   ^
 l  m   r

 1  3  -1  -2  0  4 -3  5  3  6  7
    ^       ^
   lm       r

 1  3  -1  -2  0  4 -3  5  3  6  7
        ^      ^
        l     rm

I ended up realizing that it would be easier to handle things
with a priority queue, and got that solution to work. Looking
at other solutions, the best approach seems to be deque
"""

"""
Debugs

print(f"{str(nums[left:right + 1]).ljust(k * 3 + 2)} {(left, right)} CURR {maxptr} -> {currmax} NEXT {nextmaxptr} -> {nextmax}")

print(left, right, nums[left:right + 1], [(-m, -p) for (m, p) in heap])
"""

import heapq

def max_sliding_windowv2(nums, k):
    if len(nums) == 1 and k == 1:
        return nums

    maxes = []
    heap = []

    right  = 0

    while right < k:
        heapq.heappush(heap, (-nums[right], -right))
        right += 1

    left = 1
    currmax, maxptr = heapq.heappop(heap)

    maxes.append(-currmax)

    while right < len(nums):
        if heap:
            while -maxptr < left:
                currmax, maxptr = heapq.heappop(heap)
        else:
            currmax, maxptr = -nums[right], -right

        if nums[right] >= -currmax:
            currmax = -nums[right]
            maxptr = -right
        else:
            heapq.heappush(heap, (-nums[right], -right))

        maxes.append(-currmax)

        right += 1
        left  += 1

    return maxes

from collections import deque

def max_sliding_window(nums, k):
    if len(nums) == 1 and k == 1:
        return nums

    maxes = []
    dq = deque()

    pointer = 0
    maxptr = 0
    currmax = -(10**4 + 1)

    for pointer in range(len(nums)):
        while dq and dq[0][1] < pointer - (k - 1):
            dq.popleft()

        while dq and dq[-1][0] < nums[pointer]:
            dq.pop()

        dq.append((nums[pointer], pointer))
        if pointer >= k - 1:
            maxes.append(dq[0][0])

    return maxes




test = [
    max_sliding_window([1,3,-1,-3,5,3,6,7], 3)
    , max_sliding_window([9,10,9,-7,-4,-8,2,-6], 5)
    #, max_sliding_window([7157,9172,7262,-9146,3087,5117,4046,7726,-1071,6011,5444,-48,-1385,-7328,3255,1600,586,-5160,-371,-5978,9837,3255,-6137,8587,-3403,9775,260,6016,9797,3371,2395,6851,2349,-7019,9318,1211,-3110,8735,-7507,1784,7400,-5799,3169,-7696,-8991,-2222,-9434,-4490,4034,-831,-9656,5488,-4395,9339,4104,-9058,-4072,-1172,1758,6878,-5570,-6380,9550,-9389,1411,2298,3516,551,9196,5215,-237,-4146,1682,4418,-4639,7759,9593,-9588,3041,9208,-7331,-797,-2529,7738,-2944,4351,5091,-9448,-5404,6200,-1425,-3983,678,8456,-8085,5162,7165,4692,-494,-9249,8514,521,-8835,6745,-5775,-575,1876,-5464,5053,5567,3456,5873,1965,4316,2126,9462,-59,6544,-1547,7015,-8928,-3903,-3020,5865,-9479,6723,9214,5705,5136,7725,945,-1995,-2288,4579,7103,9938,4495,-730,-3180,7717,6824,794,-894,-1439,-1641,-4577,9362,-8817,-6035,-7980,-1278,-1928,-5390,-2342,1189,-2340,4788,-1814,5927,3115,9017,6801,7884,-5719,5992,7477,-486,-2734,-1557,3169,5288,-8295,-5651,2491,-3394,8302,-8822,5638,7654,7350,9884,-5392,881,-4874,5582,8309,-8514], 45)
    #, max_sliding_window([41,8467,6334,6500,9169,5724,1478,9358,6962,4464,5705,8145,3281,6827,9961,491,2995,1942,4827,5436,2391,4604,3902,153,292,2382,7421,8716,9718,9895,5447,1726,4771,1538,1869,9912,5667,6299,7035,9894,8703,3811,1322,333,7673,4664,5141,7711,8253,6868,5547,7644,2662,2757,37,2859,8723,9741,7529,778,2316,3035,2190,1842,288,106,9040,8942,9264,2648,7446,3805,5890,6729,4370,5350,5006,1101,4393,3548,9629,2623,4084,9954,8756,1840,4966,7376,3931,6308,6944,2439,4626,1323,5537,1538,6118,2082,2929,6541,4833,1115,4639,9658,2704,9930,3977,2306,1673,2386,5021,8745,6924,9072,6270,5829,6777,5573,5097,6512,3986,3290,9161,8636,2355,4767,3655,5574,4031,2052,7350,1150,6941,1724,3966,3430,1107,191,8007,1337,5457,2287,7753,383,4945,8909,2209,9758,4221,8588,6422,4946,7506,3030,6413,9168,900,2591,8762,1655,7410,6359,7624,537,1548,6483,7595,4041,3602,4350,291,836,9374,1020,4596,4021,7348,3199,9668,4484,8281,4734,53,1999,6418,7938,6900,3788,8127,467,3728,4893,4648,2483,7807,2421,4310,6617,2813,9514,4309,7616,8935,7451,600,5249,6519,1556,2798,303,6224,1008,5844,2609,4989,2702,3195,485,3093,4343,523,1587,9314,9503,7448,5200,3458,6618,580,9796,4798,5281,9589,798,8009,7157,472,3622,8538,2292,6038,4179,8190,9657,7958,6191,9815,2888,9156,1511,6202,2634,4272,55,328,2646,6362,4886,8875,8433,9869,142,3844,1416,1881,1998,322,8651,21,5699,3557,8476,7892,4389,5075,712,2600,2510,1003,6869,7861,4688,3401,9789,5255,6423,5002,585,4182,285,7088,1426,8617,3757,9832,932,4169,2154,5721,7189,9976,1329,2368,8692,1425,555,3434,6549,7441,9512,145,8060,1718,3753,6139,2423,6279,5996,6687,2529,2549,7437,9866,2949,193,3195,3297,416,8286,6105,4488,6282,2455,5734,8114,1701,1316,671,5786,2263,4313,4355,1185,53,912,808,1832,945,4313,7756,8321,9558,3646,7982,481,4144,3196,222,7129,2161,5535,450,1173,466,2044,1659,6292,6439,7253,24,6154,9510,4745,649,3186,8313,4474,8022,2168,4018,8787,9905,7958,7391,202,3625,6477,4414,9314,5824,9334,5874,4372,159,1833,8070,7487,8297,7518,8177,7773,2270,1763,2668,7192,3985,3102,8480,9213,7627,4802,4099,527,2625,1543,1924,1023,9972,3061,4181,1003,7432,7505,7593,2725,3031,8492,142,7222,1286,3064,7900,9187,8360,2413,974,4270,9170,235,833,9711,5760,8896,4667,7285,2550,140,3694,2695,1624,8019,2125,6576,1694,2658,6302,7371,2466,4678,2593,3851,5484,1018,8464,1119,3152,2800,8087,1060,1926,9010,4757,2170,315,9576,227,2043,2758,7164,5109,7882,7086,9565,3487,9577,4474,2625,5627,5629,1928,5423,8520,6902,4962,123,4596,3737,3261,195,2525,1264,8260,6202,8116,5030,326,9011,771,6411,5547,1153,1520,9790,4924,188,1763,4940,851,8662,3829,900,7713,8958,7578,8365,3007,1477,1200,6058,6439,2303,2760,9357,2324,6477,5108], 5)
]

"""
GRAVEYARD:

def max_sliding_window(nums, k):
    if len(nums) == 1 and k == 1:
        return nums

    maxes = []

    pointer = 0

    while pointer <= len(nums) - k:
        maxes.append(
            max(nums[pointer : pointer + k])
        )

        pointer += 1

    return maxes

def max_sliding_window(nums, k):
    if len(nums) == 1 and k == 1:
        return nums

    maxes = []

    right      = 0
    maxptr     = 0
    nextmaxptr = 0

    currmax = -(10**4 + 1)
    nextmax = -(10**4 + 1)

    while right < k:
        if nums[right] >= currmax:
            maxptr = right
            currmax = nums[right]
        if nextmax <= nums[right] < currmax:
            nextmaxptr = right
            nextmax = nums[right]

        right += 1

    left = 1
    maxes.append(currmax)

    while right < len(nums):
        if maxptr < left:
            currmax = nextmax
            maxptr  = nextmaxptr
        if nextmaxptr == maxptr:
            nextmax = (-10**4 + 1)
            nextmaxptr = left
        if nextmax <= nums[right] < currmax:
            nextmaxptr = right
            nextmax = nums[right]
        if nums[right] >= currmax:
            currmax = nums[right]
            maxptr = right

        #print(f"{str(nums[left:right + 1]).ljust(k * 3 + 2)} {(left, right)} CURR {maxptr} -> {currmax} NEXT {nextmaxptr} -> {nextmax}")

        maxes.append(currmax)

        right += 1
        left  += 1

    return maxes
"""
