import time

import node
import algorithm
import config
from rendering import draw
import gameSystem
from benchmark import run_benchmarks

ALGORITHMS = (
    ("Brute Force", algorithm.brute_force_tsp, {}),
    ("Nearest Neighbor", algorithm.nearest_neighbor_tsp, {}),
    ("Held-Karp", algorithm.held_karp_tsp, {}),
    ("two-opt", algorithm.two_opt_tsp, {}),
    # ("ACO (30 iterations)", algorithm.ant_colony_tsp, {"iterations": 30}),
    # ("ACO (25 iterations)", algorithm.ant_colony_tsp, {"iterations": 25}),
    ("ACO (20 iterations)", algorithm.ant_colony_tsp, {"iterations": 20}),
    # ("ACO (15 iterations)", algorithm.ant_colony_tsp, {"iterations": 15}),
    # ("ACO (10 iterations)", algorithm.ant_colony_tsp, {"iterations": 10}),
    # ("ACO (5 iterations)", algorithm.ant_colony_tsp, {"iterations": 5}),
)

# --Main--
def main():
    if config.benchmarkMode:
        run_benchmarks(ALGORITHMS)
        return

    nodeList = node.generateNode(config.nodeCount)

    # Algorithm
    for name, fn, kwargs in ALGORITHMS:
        Result = fn(nodeList, **kwargs)
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
