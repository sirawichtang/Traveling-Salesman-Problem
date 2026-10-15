import time

import node
import config
from rendering import draw
import gameSystem
from benchmark import ALGORITHMS, run_benchmarks


# --Main--
def main():
    if config.benchmarkMode:
        run_benchmarks()
        return

    nodeList = node.generateNode(config.nodeCount)

    # Algorithm
    for name, fn in ALGORITHMS:
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
