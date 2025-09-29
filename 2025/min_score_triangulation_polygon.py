"""
1039. Minimum Score Triangulation of Polygon
https://leetcode.com/problems/minimum-score-triangulation-of-polygon/description/

You have a convex n-sided polygon where each vertex has an integer value. You are given an integer array values where values[i] is the value of the ith vertex in clockwise order.

Polygon triangulation is a process where you divide a polygon into a set of triangles and the vertices of each triangle must also be vertices of the original polygon. Note that no other shapes other than triangles are allowed in the division. This process will result in n - 2 triangles.

You will triangulate the polygon. For each triangle, the weight of that triangle is the product of the values at its vertices. The total score of the triangulation is the sum of these weights over all n - 2 triangles.

Return the minimum possible score that you can achieve with some triangulation of the polygon.


Example 1:

Input: values = [1,2,3]

Output: 6

Explanation: The polygon is already triangulated, and the score of the only triangle is 6.

Example 2:
Input: values = [3,7,4,5]

Output: 144

Explanation: There are two triangulations, with possible scores: 3*7*5 + 4*5*7 = 245, or 3*4*5 + 3*4*7 = 144.
The minimum score is 144.

Example 3:
Input: values = [1,3,1,4,1,5]

Output: 13

Explanation: The minimum score triangulation is 1*1*3 + 1*1*4 + 1*1*5 + 1*1*1 = 13.

Constraints:

n == values.length
3 <= n <= 50
1 <= values[i] <= 100
"""


import matplotlib.pyplot as plt
import numpy as np

def plot_regular_polygon(n, triangle_sets=None):
    if n < 3:
        raise ValueError("A polygon must have at least 3 sides.")

    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = np.cos(angles)
    y = np.sin(angles)

    x_closed = np.append(x, x[0])
    y_closed = np.append(y, y[0])

    num_sets = len(triangle_sets)
    cols = min(num_sets, 3)
    rows = int(np.ceil(num_sets / cols))

    fig, axs = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))
    axs = axs.flatten()

    for i, triangle_set in enumerate(triangle_sets):
        ax = axs[i]
        ax.plot(x_closed, y_closed, 'b-', linewidth=2)
        ax.fill(x_closed, y_closed, alpha=0.1, color='blue')
        ax.scatter(x, y, color='red')

        for tri in triangle_set:
            if len(tri) != 3:
                raise ValueError(f"Triangle {tri} does not have 3 vertices.")
            if any(not (0 <= idx < n) for idx in tri):
                raise ValueError(f"Triangle {tri} has invalid vertex indices.")
            tri_x = [x[idx] for idx in tri] + [x[tri[0]]]
            tri_y = [y[idx] for idx in tri] + [y[tri[0]]]
            ax.plot(tri_x, tri_y, 'g--', linewidth=1.5)
            ax.fill(tri_x, tri_y, alpha=0.2, color='green')

        ax.set_title(f"Triangle Set {i + 1}")
        ax.set_aspect('equal')
        ax.grid(True)

    # Hide unused subplots
    for j in range(len(triangle_sets), len(axs)):
        fig.delaxes(axs[j])

    plt.tight_layout()
    plt.show()

from math import factorial

def catalan_number(n):
    """
    A000108
    Catalan numbers
        C(n) = binomial(2n,n)/(n+1) = (2n)!/(n!(n+1)!)
    """
    return (
        factorial(2 * n)
            // (factorial(n) * factorial(n + 1))
    )

def adjacent_triangulation(n):
    triangles = []
    for i in range(n):
        s = []
        for k in range(n - 2):
            s.append([
                i, (i + k + 1) % n, (i + k + 2) % n
            ])
        triangles.append(s)

    return triangles

def center_triangulation(n):
    triangles = []
    for skip in range(2, n // 2):
        for i in range(n - 4):
            center = [i, i + skip, i + (2 * skip)]
            s = [center]
            for c in center:
                s.append([
                    c, (c + 1) % n, (c + 2) % n
                ])
            triangles.append(s)
    return triangles

def adj_triangle_at_vertex(i, n):
    return ((i - 1) % n, i, (i + 1) % n)

def idxs_without_vertex(i, n, idxs=None):
    if not idxs:
        return [j for j in range(n) if j != i]
    else:
        return [j for j in idxs if j != i]

def feed_vertex_via_index(opts, idxs):
    return [
        tuple(
            tuple(sorted([idxs[i] for i in o]))
            for o in opt
        )
        for opt in opts
    ]

def ear_triangulation(n, idxs=None):
    triangles = []

    if n == 4:
        opts = adjacent_triangulation(4)[:2]
        return (
            feed_vertex_via_index(opts, idxs)
            if idxs is not None
            else opts
        )
    if n == 5:
        opts = adjacent_triangulation(5)
        return (
            feed_vertex_via_index(opts, idxs)
            if idxs is not None
            else opts
        )

    for i in (
        range(n)
        if not idxs else
        idxs
    ):
        ear = adj_triangle_at_vertex(i, n)
        if idxs:
            if ear[0] not in idxs:
                continue
        print(i, n, ear, idxs_without_vertex(i, n, idxs))
        opts = ear_triangulation(
            n - 1, idxs=idxs_without_vertex(i, n, idxs)
        )
        print(opts)

        triangles.extend([
            tuple([ear, *opt])
            for opt in opts if ear not in opt
        ])

    return set([
        tuple(sorted(tuple(sorted(i)) for i in opt))
        for opt in triangles
    ])


def min_score(values):
    if len(values) < 3:
        return 0
    if len(values) == 3:
        return sum(values)

    


test = [
    min_score([1,2,3]) # 6
    , min_score([3,7,4,5]) # 144
    , min_score([1,3,1,4,1,5]) # 13
]
