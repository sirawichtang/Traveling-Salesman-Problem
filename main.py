import time

import algorithm
import node
import config
from rendering import draw
import gameSystem

# --Main--
def main():
    nodeList = node.generateNode(config.nodeCount)

    Result = algorithm.brute_force_tsp(nodeList)
    print(f"TotalDist = {Result[1]}, Iteration = {Result[2]}")

    # Draw on screen
    draw(nodeList, Result[0], Result[2], "Brute Force", Result[1], True)
    time.sleep(5)

    Result = algorithm.ant_colony_tsp(nodeList)
    print(f"TotalDist = {Result[1]}, Iteration = {Result[2]}")

    for name, fn in (("Nearest Neighbor", algorithm.nearest_neighbor_tsp), ("Held-Karp", algorithm.held_karp_tsp)):
        Result = fn(nodeList)
        print(f"{name}: TotalDist = {Result[1]}, Iteration = {Result[2]}")
        draw(nodeList, Result[0], Result[2], name, Result[1], True)
        time.sleep(5)

    waitQuit = False
    while not waitQuit:
        # Draw on screen
        draw(nodeList, Result[0], Result[2], "ACO", Result[1], True)
        waitQuit = gameSystem.quitInterrupt()

if __name__ == "__main__":
    main()