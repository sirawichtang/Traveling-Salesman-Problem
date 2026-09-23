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
nodeCount = 11
nodeSize = 5

# Optimization
doDraw = True

tickrate = 1/20