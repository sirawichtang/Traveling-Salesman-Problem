import pygame
import math
import random

# temp
import time

pygame.init()
screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
width = screen.get_width()
height = screen.get_height()

# Camera setting
CamSensitivity = 1
CamZoom = 1
CamOffsets = pygame.Vector2(width / -2, height / -2)

# Environment setting
mapSize = pygame.Vector2(500, 500)
nodeCount = 8
nodeSize = 5

#Optimization
doDraw = False

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
def draw(route, ForceDraw : bool):
    if not ForceDraw and not doDraw: return

    routeColor = "grey"
    routeWidth = 2

    screen.fill("white")

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

    # Flip
    pygame.display.flip()

    # Emergency exit (Not scuffed at all)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()

    # # Camera movement (Dont work because I am stupid)
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     CamOffsets.y += CamSensitivity / CamZoom
    # if keys[pygame.K_s]:
    #     CamOffsets.y -= CamSensitivity / CamZoom
    # if keys[pygame.K_a]:
    #     CamOffsets.x -= CamSensitivity / CamZoom
    # if keys[pygame.K_d]:
    #     CamOffsets.x += CamSensitivity / CamZoom

    # if keys[pygame.K_q]:
    #     CamZoom += CamSensitivity / 500
    # if keys[pygame.K_e]:
    #     CamZoom -= CamSensitivity / 500


# function to check the distance of the route, input a list of object as a path from first index to last index
def checkDist(route: list[Node]):
    totalDist = 0
    for i in range(len(route) - 1):
        totalDist += route[i].location.distance_to(route[i + 1].location)
    # return home
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

    best_route = [None]
    best_length = [math.inf]

    iterationCount = 0

    def permute(remaining, current):
        nonlocal iterationCount
        # base case: no more cities to place, evaluate this full route
        if not remaining:
            iterationCount += 1
            route = [home] + current
            length = checkDist(route)
            if length < best_length[0]:
                best_length[0] = length
                best_route[0] = route
            return

        # try each remaining city as the next step
        for i in range(len(remaining)):
            next_city = remaining[i]
            new_remaining = remaining[:i] + remaining[i + 1 :]  # delete chosen city
            current.append(next_city)  # insert into partial route
            permute(new_remaining, current)
            current.pop()  # backtrack: undo insert before trying next option
            try: draw([home] + current, False)
            except: pass

    permute(others, [])
    return best_route[0], best_length[0], iterationCount

# =============================================================================================
# =============================================================================================
# =============================================================================================


# --Main--
def main():

    Result = brute_force_tsp(nodeList)
    route = Result[0]
    draw(route, True)
    print(f"TotalDist = {Result[1]}, Iteration = {Result[2]}")

main()

# Quit
waitQuit = True
while waitQuit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: waitQuit = False
pygame.quit()