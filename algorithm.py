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
                draw(nodeList, best_route, iterationCount, "Brute Force", best_length, False)
                if config.doDraw : time.sleep(config.tickrate)
                

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
    iterations: int = 100,
    ant_count: int | None = None,
    evaporation: float = 0.5,
    alpha: float = 1.0,  # Chance ant will follow pheromone
    beta: float = 3.0,  # How strongly ants prefer closer node
):
    """
    Returns (best_route, best_length, iteration_count).
    The returned route starts with the home node and works with draw().
    """
    if not nodeList:
        raise ValueError("The node list cannot be empty.")

    home_index = next(
        (index for index, node in enumerate(nodeList) if node.ID == 0),
        None,
    )

    if home_index is None:
        raise ValueError("A home node with ID == 0 is required.")

    if len(nodeList) == 1:
        return [nodeList[home_index]], 0.0, 0

    if ant_count is None:
        ant_count = len(nodeList)

    ant_count = max(1, ant_count)
    node_total = len(nodeList)

    distances = [
        [nodeList[i].location.distance_to(nodeList[j].location) for j in range(node_total)]
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
                draw(nodeList, best_route, completed_iterations, "ACO", best_length, False)
                if config.doDraw : time.sleep(config.tickrate)

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

        completed_iterations += 1

        if gameSystem.quitInterrupt():
            pygame.quit()

    return best_route, best_length, completed_iterations