from collections import namedtuple
from dataclasses import dataclass
from typing import List
import pydot

Segment = namedtuple("Segment", ['start', 'end'])

segments = [
    Segment(0, 3),
    Segment(2, 5),
    Segment(3, 6),
    # Segment(7, 8)
]


def calc_elementary_intervals(segments: List[Segment]):
    sorted_endpoints = [x.end for x in list(sorted(segments, key=lambda x: x.end))]
    elementary_intervals = []

    elementary_intervals.append((float("-inf"), sorted_endpoints[0]))
    elementary_intervals.append((sorted_endpoints[0], sorted_endpoints[0]))

    for i in range(len(sorted_endpoints) - 1):
        elementary_intervals.append((sorted_endpoints[i], sorted_endpoints[i + 1]))
        elementary_intervals.append((sorted_endpoints[i + 1], sorted_endpoints[i + 1]))

    elementary_intervals.append((sorted_endpoints[-1], float("inf")))

    return elementary_intervals


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def build(intervals, l, r):
    if l > r:
        return None

    mid = (l + r) // 2

    if l == r:
        return Node(
            intervals[mid],
            left=None,
            right=None
        )

    return Node(
        f"i-{mid}",
        left=build(intervals, l, mid),
        right=build(intervals, mid + 1, r)
    )





def plot(root: Node):
    graph = pydot.Dot('tree')

    to_visit = [root]

    while len(to_visit) > 0:
        cur = to_visit.pop(0)
        graph.add_node(pydot.Node(str(cur.value)))

        if cur.left is not None:
            graph.add_edge(pydot.Edge(str(cur.value), str(cur.left.value)))
            to_visit.append(cur.left)

        if cur.right is not None:
            graph.add_edge(pydot.Edge(str(cur.value), str(cur.right.value)))
            to_visit.append(cur.right)

    graph.write_png("output.png")

el_intervals = calc_elementary_intervals(segments)
print(el_intervals)
tree = build(el_intervals, 0, len(el_intervals) - 1)
plot(tree)
