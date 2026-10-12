import time

import algorithm
import node
import config
from rendering import draw
import gameSystem


# --Main--
def main():
    nodeList = node.generateNode(config.nodeCount)

    # Algorithm

    for name, fn in (
        ("Brute Force", algorithm.brute_force_tsp),
        ("ACO", algorithm.ant_colony_tsp),
        ("Nearest Neighbor", algorithm.nearest_neighbor_tsp),
        ("Held-Karp", algorithm.held_karp_tsp),
    ):
        Result = fn(nodeList)
        print(f"{name}: TotalDist = {Result[1]}, Iteration = {Result[2]}")
        draw(nodeList, Result[0], Result[2], name, Result[1], True)
        time.sleep(5)

    # Draw latest output + closing
    waitQuit = False
    while not waitQuit:
        # Draw on screen
        draw(nodeList, Result[0], Result[2], "", Result[1], True)
        waitQuit = gameSystem.quitInterrupt()


if __name__ == "__main__":
    main()
