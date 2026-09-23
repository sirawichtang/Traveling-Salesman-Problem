import pygame

# Return wheter the program should quit or not
def quitInterrupt():
    Quitting = False
    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Quitting = True

    return Quitting