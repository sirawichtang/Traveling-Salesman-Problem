import pygame
import random

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
nodeCount = 10
nodeSize = 5

# Benchmark settings
benchmarkMode = True
benchmarkStartNodeCount = 1 #Start
benchmarkEndNodeCount = 100 #Stop
benchmarkStepCount = 1 #Step
benchmarkRepeats = 3 #repeat per nodeCount
benchmarkMaxNodeCount = {
    "Brute Force": 12,
    "Nearest Neighbor": 100,
    "Held-Karp": 20,
    "two-opt": 100,
    # "ACO (30 iterations)": 100,
    # "ACO (25 iterations)": 100,
    "ACO (20 iterations)": 100,
    # "ACO (15 iterations)": 100,
    # "ACO (10 iterations)": 100,
    # "ACO (5 iterations)": 100,

}
benchmarkResultsFile = "benchmark_results.csv"

# Optimization
doDraw = True