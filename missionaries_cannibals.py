# Missionaries and cannibals solved with breadth-first search.
#
# A state is (m, c, b):
#   m = missionaries on the left bank (0-3)
#   c = cannibals on the left bank (0-3)
#   b = 1 if the boat is on the left bank, 0 if it is on the right bank
# The right bank holds (3 - m, 3 - c). Everyone starts on the left bank.

import os
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx

START = (3, 3, 1)
GOAL = (0, 0, 0)

# Possible boat loads as (missionaries, cannibals).
LOADS = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]


def is_valid(state):
    """A state is valid if counts are in range and no bank has missionaries outnumbered."""
    m, c, _ = state
    if not (0 <= m <= 3 and 0 <= c <= 3):
        return False
    left_ok = m == 0 or m >= c
    right_ok = 3 - m == 0 or 3 - m >= 3 - c
    return left_ok and right_ok


def successors(state):
    """Valid states reachable with one boat crossing."""
    m, c, b = state
    direction = -1 if b == 1 else 1  # leaving the left bank removes people from it
    result = []
    for dm, dc in LOADS:
        new_state = (m + direction * dm, c + direction * dc, 1 - b)
        if is_valid(new_state):
            result.append(new_state)
    return result


def bfs(start, goal):
    """Return the shortest list of states from start to goal, or None if there is none."""
    parent = {start: None}
    frontier = deque([start])
    while frontier:
        state = frontier.popleft()
        if state == goal:
            path = []
            while state is not None:
                path.append(state)
                state = parent[state]
            return path[::-1]
        for next_state in successors(state):
            if next_state not in parent:  # skip repeated states
                parent[next_state] = state
                frontier.append(next_state)
    return None


def state_space(start):
    """Return (depth of each reachable state, set of edges between reachable states)."""
    depth = {start: 0}
    edges = set()
    frontier = deque([start])
    while frontier:
        state = frontier.popleft()
        for next_state in successors(state):
            edges.add(frozenset((state, next_state)))
            if next_state not in depth:
                depth[next_state] = depth[state] + 1
                frontier.append(next_state)
    return depth, edges


def draw_state_space(filename):
    """Draw every reachable state and crossing and save the picture as a PNG."""
    depth, edges = state_space(START)
    graph = nx.Graph()
    for state, d in depth.items():
        graph.add_node(state, layer=d)
    for edge in edges:
        graph.add_edge(*edge)

    pos = nx.multipartite_layout(graph, subset_key="layer")
    labels = {state: f"({state[0]},{state[1]},{state[2]})" for state in graph.nodes}

    plt.figure(figsize=(16, 6))
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_nodes(graph, pos, node_size=1800, node_color="lightblue", edgecolors="black")
    nx.draw_networkx_labels(graph, pos, labels, font_size=9)
    plt.title("Missionaries and cannibals state space (m, c, b)")
    plt.axis("off")
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    plt.savefig(path, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    for state in bfs(START, GOAL):
        print(state)
    draw_state_space("missionaries_cannibals_state_space.png")
