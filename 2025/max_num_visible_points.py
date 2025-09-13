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
from collections import Counter

def normalize(v):
    if isinstance(v, list):
        v = np.array(v)

    norm = np.linalg.norm(v)
    if norm == 0:
        return np.zeros_like(v)

    return v / norm

def get_angle(v):
    angle = np.arctan2(*reversed(normalize(v)))

    if angle < 0:
        angle = np.pi + (np.pi + angle)

    return angle % (2 * np.pi)

def get_initial_fov(angle):
    return np.array([0, np.radians(angle)])

# NOTE: had to look up arange, forgot about it
def get_scan_range(step=0.01):
    return np.arange(0, 2 * np.pi + step, step)

def get_point_angles(points):
    return np.array([
        get_angle(p) for p in points
    ])

def is_close_or_greater(a, b, atol=1e-3):
    return np.isclose(a, b, atol=atol) | (a > b)

def is_close_or_less(a, b, atol=1e-3):
    return np.isclose(a, b, atol=atol) | (a < b)

def is_angle_in_fov(angle, fov):
    angle_min, angle_max = fov
    angle_min = angle_min % (2 * np.pi)
    angle_max = angle_max % (2 * np.pi)

    if angle_min <= angle_max:
        return angle_min <= angle <= angle_max
        return is_close_or_greater(
            angle_max
            , is_close_or_greater(angle, angle_min)
        )
    else:
        return angle_min <= angle or angle >= angle_max
        return (
            is_close_or_greater(angle, angle_min)
            or is_close_or_less(angle, angle_max)
        )

def angles_in_fov(angles, fov):
    angle_min, angle_max = fov % (2 * np.pi)
    if angle_min <= angle_max:
        return angles[
            (angle_min <= angles)
            & (angles <= angle_max)
        ].shape[0]
        return angles[(
            is_close_or_greater(angles, angle_min)
            & is_close_or_less(angles, angle_max)
        )].shape[0]
    else:
        return angles[
            (angle_min <= angles)
            | (angles >= angle_max)
        ].shape[0]
        return angles[(
            is_close_or_greater(angles, angle_min)
            | is_close_or_less(angles, angle_max)
        )].shape[0]

def num_points_in_fov(angles, fov):
    return angles_in_fov(angles, fov)
    return angles[(
        is_close_or_greater(angles, fov[0])
        & is_close_or_less(angles, fov[1])
    )
    ].shape[0]
    #return angles[[
    #    is_angle_in_fov(angle, fov)
    #    for angle in angles
    #]].shape[0]

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

    offsets = offset_points_by_location(points, location)

    angles = get_point_angles(
        offsets
    )

    if angle == 0:
        counts = 0
        for ((x, y), count) in Counter([
            tuple(np.round(normalize(v), 4))
            for v in offsets
        ]).most_common():
            if x == y:
                counts += count

        return counts

    return max([
        num_points_in_fov(angles, fov)
        for fov in get_fov_map(get_initial_fov(angle))
    ])

test = [
    visible_points([[2,1],[2,2],[3,3]], 90, [1,1])
    , visible_points([[2,1],[2,2],[3,4],[1,1]], 90, [1,1])
    , visible_points([[1,1],[2,2],[3,3],[4,4],[1,2],[2,1]], 0, [1,1])
    , visible_points([[0, 0], [0,2]], 90, [1,1])
    , visible_points([[60,61],[58,47],[17,26],[87,97],[63,63],[26,50],[70,21],[3,89],[51,24],[55,14],[6,51],[64,21],[66,33],[54,35],[87,38],[30,0],[37,92],[92,12],[60,73],[75,98],[1,11],[88,24],[82,92]], 44, [15,50])
    , visible_points([[41,7],[22,94],[90,53],[94,54],[58,50],[51,96],[87,88],[55,98],[65,62],[36,47],[91,61],[15,41],[31,94],[82,80],[42,73],[79,6],[45,4]], 17, [6,84])
    , visible_points([[33,20],[74,31],[15,84],[97,5],[39,9],[75,82],[87,77],[43,80],[43,39],[69,32],[56,69],[17,94],[64,37],[90,35],[3,87],[83,90],[51,72],[52,100],[100,16],[40,62],[25,52],[67,60],[9,89],[97,41],[74,47],[76,42],[20,83],[29,20],[38,97],[73,85],[25,49],[82,22],[37,69],[48,86],[7,5],[25,70],[94,95],[13,35],[70,75],[58,93],[72,30],[73,11],[88,82],[5,24],[99,83],[91,87],[23,0],[15,55],[69,80],[17,76],[74,68],[53,21],[64,66],[100,70],[90,68],[77,5],[7,55],[18,41],[25,80],[92,66],[100,59],[37,38],[26,53],[76,6],[48,72],[68,8],[3,76],[66,47],[70,9],[23,72],[15,87],[48,79],[54,13],[80,94],[18,98],[85,42],[4,23],[1,2],[41,37],[58,56],[58,10],[72,99],[83,2],[34,59],[60,80],[61,67],[54,64],[92,9],[18,60],[20,85],[62,16],[34,67],[94,72],[0,99],[100,98],[3,10],[49,70],[10,2],[32,0],[72,10],[27,18],[6,41],[16,89],[33,30],[92,40],[100,67],[29,57],[5,27],[73,53],[87,48],[49,77],[5,70],[12,78],[92,55],[1,16],[87,6],[89,23],[36,32],[92,87],[74,33],[15,15],[79,96],[27,30],[8,98]], 57, [35,42])
]

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def plot_points(xy_points):
    """
    Plots a list of (x, y) points and returns the figure and axes.

    Parameters:
    xy_points (list of tuples): List of (x, y) points to be plotted.

    Returns:
    figure, axes: The figure and axes objects of the plot.
    """
    # Unzip the list of points into separate x and y coordinates
    x_vals, y_vals = zip(*xy_points)

    # Create a figure and axes
    fig, ax = plt.subplots()

    # Plot the points
    ax.scatter(x_vals, y_vals)

    # Optionally, set labels and title
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Scatter Plot of Points')

    # Return the figure and axes
    return fig, ax

def overlay_fov(fig, ax, fov_angle_radians, color='orange'):
    """
    Overlays a cone-shaped region representing the Field of View (FoV) on the plot.

    Parameters:
    fig (matplotlib.figure.Figure): The figure object returned from the plot_points function.
    ax (matplotlib.axes._axes.Axes): The axes object returned from the plot_points function.
    fov_angle_radians (tuple): A pair (angle_start, angle_end) in radians that defines the Field of View (FoV).
                                The cone will be shaded between these two angles.
    """
    # Extract the starting and ending angles
    angle_start, angle_end = fov_angle_radians

    # Number of points to define the cone shape
    num_points = 100

    # Generate points for the cone boundary
    angles = np.linspace(angle_start, angle_end, num_points)

    # Define the radius for the cone (for visualization purposes, let's set it arbitrarily)
    radius = 1

    # Convert polar to Cartesian coordinates (for the cone's boundary)
    x_vals = np.append([0], radius * np.cos(angles))
    y_vals = np.append([0], radius * np.sin(angles))

    # Create a polygon from these points
    cone_polygon = Polygon(list(zip(x_vals, y_vals)), closed=True, color=color, alpha=0.3)

    # Add the cone polygon to the plot
    ax.add_patch(cone_polygon)

    # Redraw the plot
    fig.canvas.draw()
    return fig, ax

def debug_plot(points, angle, location):
    offsets = offset_points_by_location(points, location)
    norms = np.array([normalize(v) for v in offsets])

    angles = get_point_angles(
        offsets
    )

    fovs = get_fov_map(get_initial_fov(angle))

    res = np.array([
        num_points_in_fov(angles, fov)
        for fov in fovs
    ])
    maxval = max(res)

    wheremax = np.argwhere(res == maxval)
    fov1 = fovs[wheremax[0][0]]
    fov2 = fovs[wheremax[-1][0]]

    fig, ax = overlay_fov(*plot_points(norms), fov1)
    overlay_fov(fig, ax, fov2, color='green')
    plt.show()



"""
Notes:

Missed a case where the angle could be 0, which would mean
that this will cast a ray to the east at the starting location,
so we have to scan that ray as well

After messing around with debug-plotting and trying to fix
weird scenarios where I'm off by 1 count, I'm giving up :(
"""

"""
GRAVEYARD

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


"""
