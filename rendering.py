import pygame

import config
from node import Node

# calculate offsets and perform zoom on a vector2
def render(base):
    return pygame.Vector2(config.width / 2, config.height / 2) + (
        pygame.Vector2(
            ((config.width / 2) - (base.x - config.CamOffsets.x)) * -config.CamZoom,
            ((config.height / 2) - (base.y - config.CamOffsets.y)) * config.CamZoom,
        )
    )


# draw borders, node etc
def draw(nodeList : list[Node], route: list[Node], iterationCount : int, algorithmType : str, bestLength : float, ForceDraw : bool):
    if not ForceDraw and not config.doDraw:
        return

    routeColor = "grey"
    routeWidth = 2

    config.screen.fill("white")

    # Draw Text
    text_algorithmType = config.my_font.render(algorithmType, False, "Black")
    config.screen.blit(text_algorithmType, (0,0))
    text_IterationCount = config.my_font.render(f"IterationCount = {iterationCount}", False, "Black")
    config.screen.blit(text_IterationCount, (0,16))
    text_bestLength = config.my_font.render(f"bestLength = {bestLength}", False, "Black")
    config.screen.blit(text_bestLength, (0,32))

    # Draw borders
    pygame.draw.lines(
        config.screen,
        "black",
        True,
        [
            render(pygame.Vector2(config.mapSize.x / 2, config.mapSize.y / 2)),
            render(pygame.Vector2(-config.mapSize.x / 2, config.mapSize.y / 2)),
            render(pygame.Vector2(-config.mapSize.x / 2, -config.mapSize.y / 2)),
            render(pygame.Vector2(config.mapSize.x / 2, -config.mapSize.y / 2)),
        ],
    )
    # Draw nodes
    for n in nodeList:
        if n.ID == 0:
            pygame.draw.circle(config.screen, "green", render(n.location), config.nodeSize * config.CamZoom)
        else:
            pygame.draw.circle(config.screen, "red", render(n.location), config.nodeSize * config.CamZoom)

    # Draw route
    for i in range(len(route) - 1):
        pygame.draw.line(
            config.screen,
            routeColor,
            render(route[i].location),
            render(route[i + 1].location),
            routeWidth,
        )

    pygame.draw.line(
        config.screen,
        routeColor,
        render(route[-1].location),
        render(route[0].location),
        routeWidth,
    )

    pygame.display.flip()