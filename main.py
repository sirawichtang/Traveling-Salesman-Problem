import pygame
import math
import random

# temp
import time

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 16)
screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
width = screen.get_width()
height = screen.get_height()

# Camera setting
CamSensitivity = 1
CamZoom = 1
CamOffsets = pygame.Vector2(width / -2, height / -2)

# Environment setting
random.seed(None)

mapSize = pygame.Vector2(800, 800)
nodeCount = 11
nodeSize = 5

# Optimization
doDraw = True

tickrate = 1/20


class Node:
    def __init__(self, ID: int):
        self.ID = ID
        self.location = pygame.Vector2(
            random.uniform(-mapSize.x / 2, mapSize.x / 2),
            random.uniform(-mapSize.y / 2, mapSize.y / 2),
        )


# creaing a node obj
nodeList: list[Node] = []
for n in range(nodeCount):
    nodeList.append(Node(n))


# calculate offsets and perform zoom on a vector2
def render(base):
    return pygame.Vector2(width / 2, height / 2) + (
        pygame.Vector2(
            ((width / 2) - (base.x - CamOffsets.x)) * -CamZoom,
            ((height / 2) - (base.y - CamOffsets.y)) * CamZoom,
        )
    )


# draw borders, node etc
def draw(route, iterationCount, algorithmType, bestLength, ForceDraw: bool):
    if not ForceDraw and not doDraw:
        return

    routeColor = "grey"
    routeWidth = 2

    screen.fill("white")

    # Draw Text
    text_algorithmType = my_font.render(algorithmType, False, "Black")
    screen.blit(text_algorithmType, (0,0))
    text_IterationCount = my_font.render(f"IterationCount = {iterationCount}", False, "Black")
    screen.blit(text_IterationCount, (0,16))
    text_bestLength = my_font.render(f"bestLength = {bestLength}", False, "Black")
    screen.blit(text_bestLength, (0,32))

    # Draw borders
    pygame.draw.lines(
        screen,
        "black",
        True,
        [
            render(pygame.Vector2(mapSize.x / 2, mapSize.y / 2)),
            render(pygame.Vector2(-mapSize.x / 2, mapSize.y / 2)),
            render(pygame.Vector2(-mapSize.x / 2, -mapSize.y / 2)),
            render(pygame.Vector2(mapSize.x / 2, -mapSize.y / 2)),
        ],
    )
    # Draw nodes
    for n in nodeList:
        if n.ID == 0:
            pygame.draw.circle(screen, "green", render(n.location), nodeSize * CamZoom)
        else:
            pygame.draw.circle(screen, "red", render(n.location), nodeSize * CamZoom)

    # Draw route
    for i in range(len(route) - 1):
        pygame.draw.line(
            screen,
            routeColor,
            render(route[i].location),
            render(route[i + 1].location),
            routeWidth,
        )

    pygame.draw.line(
        screen,
        routeColor,
        render(route[-1].location),
        render(route[0].location),
        routeWidth,
    )

    pygame.display.flip()


# Return wheter the program should quit or not
def quitInterrupt():
    Quitting = False
    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Quitting = True

    return Quitting

def waitKey():
    pass


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


def brute_force_tsp(nodes):
    """
    nodes: list of Node objects, must include the Home node (ID == 0).
    Returns (best_route, best_length).
    """
    home = next(n for n in nodes if n.ID == 0)
    others = [n for n in nodes if n.ID != 0]

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
                draw(best_route, iterationCount, "Brute Force", best_length, False)
                if doDraw : time.sleep(tickrate)
                

            return

        # Try each remaining city as the next step
        for i in range(len(remaining)):
            next_city = remaining[i]
            new_remaining = remaining[:i] + remaining[i + 1 :]  # delete chosen city
            current.append(next_city)  # insert into partial route
            permute(new_remaining, current)
            current.pop()  # backtrack: undo insert before trying next option

        if quitInterrupt():
            pygame.quit()

    permute(others, [])
    return best_route, best_length, iterationCount


def ant_colony_tsp(
    nodes: list[Node],
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
    if not nodes:
        raise ValueError("The node list cannot be empty.")

    home_index = next(
        (index for index, node in enumerate(nodes) if node.ID == 0),
        None,
    )

    if home_index is None:
        raise ValueError("A home node with ID == 0 is required.")

    if len(nodes) == 1:
        return [nodes[home_index]], 0.0, 0

    if ant_count is None:
        ant_count = len(nodes)

    ant_count = max(1, ant_count)
    node_total = len(nodes)

    distances = [
        [nodes[i].location.distance_to(nodes[j].location) for j in range(node_total)]
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

            route = [nodes[index] for index in route_indices]
            length = checkDist(route)
            iteration_routes.append((route, length))

            if length < best_length:
                best_route = route[:]
                best_length = length

                # Draw the newest best route.
                draw(best_route, completed_iterations, "ACO", best_length, False)
                if doDraw : time.sleep(tickrate)

        # Evaporate pheromone.
        for i in range(node_total):
            for j in range(node_total):
                pheromone[i][j] *= 1.0 - evaporation
                pheromone[i][j] = max(pheromone[i][j], 0.000001)

        # Deposit pheromone for every ant's route.
        for route, length in iteration_routes:
            deposit = 1.0 / max(length, 0.000001)

            for i in range(len(route)):
                current = nodes.index(route[i])
                next_node = nodes.index(route[(i + 1) % len(route)])

                pheromone[current][next_node] += deposit
                pheromone[next_node][current] += deposit

        completed_iterations += 1

    return best_route, best_length, completed_iterations


# =============================================================================================
# =============================================================================================
# =============================================================================================


# --Main--
waitQuit = False
if __name__ == "__main__":

    Result = brute_force_tsp(nodeList)
    print(f"TotalDist = {Result[1]}, Iteration = {Result[2]}")

    # Draw on screen
    draw(Result[0], Result[2], "Brute Force", Result[1], True)
    time.sleep(5)

    Result = ant_colony_tsp(nodeList)
    print(f"TotalDist = {Result[1]}, Iteration = {Result[2]}")

    while not waitQuit:
        # Draw on screen
        draw(Result[0], Result[2], "ACO", Result[1], True)
        waitQuit = quitInterrupt()
