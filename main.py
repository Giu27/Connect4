import pygame as pg
import sys
from settings import *

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT), 0, 32)
pg.display.set_caption("Connect 4!")

clock = pg.Clock()

grid = [[0 for column in range(COLUMNS)] for row in range(ROWS)]

def drawGrid():
    sideOffset = int(WIDTH * (SIDE_PADDING / 100))
    topOffset = int(HEIGHT * (TOP_PADDING / 100))
    bottomOffset = int(HEIGHT * (BOTTOM_PADDING / 100))
    actualWidth = WIDTH - sideOffset * 2
    actualHeight = HEIGHT - topOffset - bottomOffset
    hStep = (actualWidth - 2 * RADIUS) / (COLUMNS - 1) if COLUMNS > 1 else 0
    vStep = (actualHeight - 2 * RADIUS) / (ROWS - 1) if ROWS > 1 else 0

    
    for r in range(ROWS):
        for c in range(COLUMNS):
            center = (RADIUS + sideOffset + hStep * c , RADIUS + topOffset  + vStep * r)
            pg.draw.circle(screen, EMPTY_COLOUR, center, RADIUS)
            if DEBUG: 
                pg.draw.line(screen, "red", (0,10), (sideOffset, 10))
                pg.draw.line(screen, "red", (WIDTH,10), (WIDTH - sideOffset, 10))
                pg.draw.line(screen, "green", (sideOffset, 0), (sideOffset, topOffset))
                pg.draw.line(screen, "green", (WIDTH - sideOffset, 0), (WIDTH - sideOffset, topOffset))
                pg.draw.line(screen, "green", (sideOffset, HEIGHT), (sideOffset, HEIGHT - bottomOffset))
                pg.draw.line(screen, "green", (WIDTH - sideOffset, HEIGHT), (WIDTH - sideOffset, HEIGHT - bottomOffset))
                pg.draw.line(screen, "red", center, (center[0], 10))
                pg.draw.line(screen, "green", (center[0] - RADIUS, center[1] - RADIUS), (center[0] + RADIUS, center[1] - RADIUS))
                pg.draw.line(screen, "green", (center[0] - RADIUS, center[1] + RADIUS), (center[0] + RADIUS, center[1] + RADIUS))

if __name__ == "__main__":
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    DEBUG = not DEBUG

        screen.fill(BACKGROUND_COLOUR)

        drawGrid()

        clock.tick(FPS)
        pg.display.update()