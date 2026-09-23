import pygame
import random

from config import mapSize

class Node:
    def __init__(self, ID: int):
        self.ID = ID
        self.location = pygame.Vector2(
            random.uniform(-mapSize.x / 2, mapSize.x / 2),
            random.uniform(-mapSize.y / 2, mapSize.y / 2),
        )

 # creaing a node list
def generateNode(nodeCount : int):
    return [Node(n) for n in range(nodeCount)]