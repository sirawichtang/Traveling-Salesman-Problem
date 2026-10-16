import pygame
import time
import math
import random

from node import Node
from rendering import draw
import config
import gameSystem


# Function to check the distance of the route, input a list of object as a path from first index to last index
def checkDist(route: list[Node]):
    totalDist = 0
    for i in range(len(route) - 1):
        totalDist += route[i].location.distance_to(route[i + 1].location)
    # Return home
    totalDist += route[-1].location.distance_to(route[0].location)
    return totalDist


# =============================================================================================
# ==================Test part(AI generated for prototyping, please fix later)======================
# =============================================================================================


def brute_force_tsp(nodeList):
    """
    nodes: list of Node objects, must include the Home node (ID == 0).
    Returns (best_route, best_length).
    """
    home = next(n for n in nodeList if n.ID == 0)
    others = [n for n in nodeList if n.ID != 0]

    best_route = None
    best_length = math.inf

    iterationCount = 0

    def permute(remaining, current):
        nonlocal iterationCount, best_route, best_length

        if not remaining:
            iterationCount += 1
            route = [home] + current
            length = checkDist(route)

            if length < best_length:
                best_length = length
                best_route = route[:]

                # Draw the newest best route.
                draw(
                    nodeList,
                    best_route,
                    iterationCount,
                    "Brute Force",
                    best_length,
                    False,
                )

            return

        # Try each remaining city as the next step
        for i in range(len(remaining)):
            next_city = remaining[i]
            new_remaining = remaining[:i] + remaining[i + 1 :]  # delete chosen city
            current.append(next_city)  # insert into partial route
            permute(new_remaining, current)
            current.pop()  # backtrack: undo insert before trying next option

        if gameSystem.quitInterrupt():
            pygame.quit()

    permute(others, [])
    return best_route, best_length, iterationCount


def ant_colony_tsp(
    nodeList: list[Node],
    iterations: int = 100, # Value greater than 20 is so nelegable that it is not worth using
    ant_count: int | None = None,  # When set to None, Will use nodeCount
    evaporation: float = 0.5,
    alpha: float = 1.0,  # Chance ant will follow pheromone
    beta: float = 3.0,  # How strongly ants prefer closer node
):
    home_index = next(
        (index for index, node in enumerate(nodeList) if node.ID == 0),
        None,
    )

    if len(nodeList) == 1:
        return [nodeList[home_index]], 0.0, 0

    if ant_count is None:
        ant_count = len(nodeList)

    ant_count = max(1, ant_count)
    node_total = len(nodeList)

    distances = [
        [
            nodeList[i].location.distance_to(nodeList[j].location)
            for j in range(node_total)
        ]
        for i in range(node_total)
    ]

    pheromone = [[1.0 for _ in range(node_total)] for _ in range(node_total)]

    best_route = None
    best_length = math.inf
    completed_iterations = 0

    for _ in range(iterations):
        iteration_routes = []

        for _ in range(ant_count):
            route_indices = [home_index]
            unvisited = set(range(node_total))
            unvisited.remove(home_index)

            while unvisited:
                current = route_indices[-1]

                zero_distance_nodes = [
                    index for index in unvisited if distances[current][index] == 0
                ]

                if zero_distance_nodes:
                    next_index = random.choice(zero_distance_nodes)
                else:
                    choices = list(unvisited)
                    weights = []

                    for candidate in choices:
                        trail = pheromone[current][candidate] ** alpha
                        visibility = (1.0 / distances[current][candidate]) ** beta
                        weights.append(trail * visibility)

                    next_index = random.choices(
                        choices,
                        weights=weights,
                        k=1,
                    )[0]

                route_indices.append(next_index)
                unvisited.remove(next_index)

            route = [nodeList[index] for index in route_indices]
            length = checkDist(route)
            iteration_routes.append((route, length))

            if length < best_length:
                best_route = route[:]
                best_length = length

                # Draw the newest best route.
                draw(
                    nodeList,
                    best_route,
                    completed_iterations,
                    "ACO",
                    best_length,
                    False,
                )

            completed_iterations += 1

        # Evaporate pheromone.
        for i in range(node_total):
            for j in range(node_total):
                pheromone[i][j] *= 1.0 - evaporation
                pheromone[i][j] = max(pheromone[i][j], 0.000001)

        # Deposit pheromone for every ant's route.
        for route, length in iteration_routes:
            deposit = 1.0 / max(length, 0.000001)

            for i in range(len(route)):
                current = nodeList.index(route[i])
                next_node = nodeList.index(route[(i + 1) % len(route)])

                pheromone[current][next_node] += deposit
                pheromone[next_node][current] += deposit

        if gameSystem.quitInterrupt():
            pygame.quit()

    return best_route, best_length, completed_iterations


def nearest_neighbor_tsp(nodeList: list[Node]):
    """Greedy: from home, always go to the closest unvisited node. O(n^2), not optimal."""
    route = [next(n for n in nodeList if n.ID == 0)]
    unvisited = [n for n in nodeList if n.ID != 0]
    steps = 0

    while unvisited:
        nearest = min(
            unvisited, key=lambda n: route[-1].location.distance_to(n.location)
        )
        unvisited.remove(nearest)
        route.append(nearest)
        steps += 1

        # Draw the newest best route.
        draw(nodeList, route, steps, "Nearest Neighbor", checkDist(route), False)
        if gameSystem.quitInterrupt():
            pygame.quit()

    return route, checkDist(route), steps


def held_karp_tsp(nodeList: list[Node]):
    """
    Exact DP. dp[(mask, j)] = shortest path from home, visiting the set `mask`
    of nodes, ending at j. O(n^2 * 2^n) time, O(n * 2^n) memory.
    """
    home = next(n for n in nodeList if n.ID == 0)
    others = [n for n in nodeList if n.ID != 0]
    n = len(others)
    d = lambda a, b: a.location.distance_to(b.location)

    if n == 0:
        return [home], 0.0, 0

    dp = {
        (1 << j, j): (d(home, others[j]), None) for j in range(n)
    }  # (cost, previous node)
    steps = 0

    for mask in range(1, 1 << n):
        for j in range(n):
            if not mask & (1 << j) or (mask, j) in dp:
                continue
            prev_mask = mask ^ (1 << j)
            dp[(mask, j)] = min(
                (dp[(prev_mask, k)][0] + d(others[k], others[j]), k)
                for k in range(n)
                if prev_mask & (1 << k)
            )
            steps += 1
        if gameSystem.quitInterrupt():
            pygame.quit()

    full = (1 << n) - 1
    cost, last = min((dp[(full, j)][0] + d(others[j], home), j) for j in range(n))

    # Walk back through the stored predecessors to rebuild the route
    route, mask = [], full
    while last is not None:
        route.append(others[last])
        mask, last = mask ^ (1 << last), dp[(mask, last)][1]
    route = [home] + route[::-1]

    # Draw the newest best route.
    draw(nodeList, route, steps, "Held-Karp", cost, False)
    return route, cost, steps


def two_opt_tsp(nodeList):

    home = next(n for n in nodeList if n.ID == 0)
    others = [n for n in nodeList if n.ID != 0]

    # Random initial seed, home always stays at index 0
    best_route = [home] + random.sample(others, len(others))
    best_length = checkDist(best_route)

    iterationCount = 0
    improved = True

    # Keep doing full passes until a pass finds no shorter route
    while improved:
        improved = False
        iterationCount += 1
        seed = best_route[:]

        # Try reversing every segment seed[i..j] (start at 1 so home is never moved)
        for i in range(1, len(seed) - 1):
            for j in range(i + 1, len(seed)):
                route = seed[:i] + seed[i : j + 1][::-1] + seed[j + 1 :]
                length = checkDist(route)

                if length < best_length:
                    best_length = length
                    best_route = route
                    improved = True

                    # Draw the newest best route.
                    draw(
                        nodeList,
                        best_route,
                        iterationCount,
                        "2-opt",
                        best_length,
                        False,
                    )

        if gameSystem.quitInterrupt():
            pygame.quit()

    return best_route, best_length, iterationCount
