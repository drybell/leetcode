"""
1610. Maximum Number of Visible Points
https://leetcode.com/problems/maximum-number-of-visible-points/description/

You are given an array points, an integer angle, and your location, where location = [posx, posy] and points[i] = [xi, yi] both denote integral coordinates on the X-Y plane.

Initially, you are facing directly east from your position. You cannot move from your position, but you can rotate. In other words, posx and posy cannot be changed. Your field of view in degrees is represented by angle, determining how wide you can see from any given view direction. Let d be the amount in degrees that you rotate counterclockwise. Then, your field of view is the inclusive range of angles [d - angle/2, d + angle/2].

You can see some set of points if, for each point, the angle formed by the point, your position, and the immediate east direction from your position is in your field of view.

There can be multiple points at one coordinate. There may be points at your location, and you can always see these points regardless of your rotation. Points do not obstruct your vision to other points.

Return the maximum number of points you can see.

Input: points = [[2,1],[2,2],[3,3]], angle = 90, location = [1,1]
Output: 3
Explanation: The shaded region represents your field of view. All points can be made visible in your field of view, including [3,3] even though [2,2] is in front and in the same line of sight.
Example 2:

Input: points = [[2,1],[2,2],[3,4],[1,1]], angle = 90, location = [1,1]
Output: 4
Explanation: All points can be made visible in your field of view, including the one at your location.

Input: points = [[1,0],[2,1]], angle = 13, location = [1,1]
Output: 1
Explanation: You can only see one of the two points, as shown above.


Strategy:

Let's break the problem down into a couple sections.

1. Rotate FOV
2. Scan
3. Cache

Rotate FOV
    - Given an iteration param, rotate the viewer by angle * iteration
        * d = angle * iteration
        * fov = [d - angle/2, d + angle/2]
    - Returns the vectors bounding the fov

Scan
    - Given an fov vector, identify if points are in fov
    - How do we determine if points are in fov?

Cache
    - For every scan output, identify if the number of scanned
      points is more than the current cache size. If there are more
      scanned points, store the largest scan size

To start, we should first translate the world origin to
be the location of the viewer, and subtract each point
by this found offset (viewer coordinates)

Couple issues with this approach:
    - As I began setting up the helper functions, I got to
      the start of writing the scan function, and realized
      that there are scenarios where if we just rotated the
      viewer by some set amount every iteration, there's a chance
      we miss the optimal fov. If we then attempt to scan as
      granular as possible, the # of iterations skyrockets and
      we'll be mostly looking at empty space for each iteration
    - what we should do instead is identify the vector containing
      the average value of the points and set the fov to match
      that. Only issues would be if the points are scattered across
      the entire plane then this approach would fail
    - I think to start I'll still go with the scan by iteration
      approach, and see how slow it is

"""

import numpy as np

PI    = np.pi
TWOPI = 2 * PI

# NOTE: had to look up the 2D rotation matrix
# had the cos/sin flipped
# (Been a while...)
# ended up not using this
def rotmat(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta)]
        , [np.sin(theta), np.cos(theta)]
    ])

# ended up not using this
def rotate(v, rad):
    return rotmat(rad) @ v

def normalize(v):
    if isinstance(v, list):
        v = np.array(v)

    norm = np.linalg.norm(v)
    if norm == 0:
        return np.zeros_like(v)

    return v / norm

def get_angle(v):
    return np.arctan2(*normalize(v))

def get_initial_fov(angle):
    return np.array([0, np.radians(angle)])

# NOTE: had to look up arange, forgot about it
def get_scan_range(step=0.01):
    return np.arange(0, 2 * np.pi, step)

def get_point_angles(points):
    return np.array([
        get_angle(p) for p in points
    ])

def is_close_or_greater(a, b, atol=1e-3, rtol=1e-5):
    return np.isclose(a, b, atol=atol, rtol=rtol) | (a > b)

def is_close_or_less(a, b, atol=1e-3, rtol=1e-5):
    return np.isclose(a, b, atol=atol, rtol=rtol) | (a < b)

def num_points_in_fov(angles, fov):
    return angles[
        is_close_or_greater(angles, fov[0])
        & is_close_or_less(angles, fov[1])
    ].shape[0]

def get_fov_map(fov, steps=0.001):
    # generates a list of fov's that scans
    # the entire cartesian plane
    # assumes angle is in radians
    return np.array([
        fov + step
        for step in get_scan_range(steps)
    ])

def offset_points_by_location(points, location):
    return [
        np.array(p) - np.array(location)
        for p in points
    ]

def visible_points(points, angle, location):
    if angle == 360: # we can see everything
        return len(points)

    angles = get_point_angles(
        offset_points_by_location(points, location)
    )

    if angle == 0:
        return angles[angles == 0].shape[0]

    return max([
        num_points_in_fov(angles, fov)
        for fov in get_fov_map(get_initial_fov(angle))
    ])

test = [
    visible_points([[2,1],[2,2],[3,3]], 90, [1,1])
    , visible_points([[2,1],[2,2],[3,4],[1,1]], 90, [1,1])
    , visible_points([[1,1],[2,2],[3,3],[4,4],[1,2],[2,1]], 0, [1,1])
]

"""
Notes:

Missed a case where the angle could be 0, which would mean
that this will cast a ray to the east at the starting location,
so we have to scan that ray as well
"""
