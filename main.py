import pygame as pg
import sys
from settings import *
from utils import *

pg.init()

class Counter(pg.sprite.Sprite):
    def __init__(self, player : int, gridPos : tuple[int, int]):
        super().__init__()
        self.image = pg.Surface((RADIUS * 2, RADIUS * 2), pg.SRCALPHA, 32)
        colour = PLAYER1_COLOUR if player == 1 else PLAYER2_COLOUR
        pg.draw.circle(self.image, colour, (RADIUS, RADIUS), RADIUS)

        inner_colour = PLAYER1_INNER_COLOUR if player == 1 else PLAYER2_INNER_COLOUR
        inner_radius = RADIUS * (1 - BORDER_PERCENTAGE / 100)
        pg.draw.circle(self.image, inner_colour, (RADIUS, RADIUS), inner_radius)

        self.target = calculateCounterCenter(gridPos[0], gridPos[1], sideOffset, topOffset, bottomOffset)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self.target[0] - RADIUS, topOffset)

        self.speedBoost = STARTING_MULTIPLIER

        self.placed = False

    def update(self):
        if self.rect.center[1] < self.target[1] and not self.placed:
            self.rect.y += BASE_SPEED * self.speedBoost
            self.speedBoost += MULTIPLIER_INCREASE
        else:
            self.placed = True
            self.rect.center = self.target
            self.speedBoost = STARTING_MULTIPLIER

screen = pg.display.set_mode((WIDTH, HEIGHT), 0, 32)
pg.display.set_caption("Connect 4!")

clock = pg.Clock()

grid = [[0 for column in range(COLUMNS)] for row in range(ROWS)] #Will be used by the actual logic of the game

counters = pg.sprite.Group(Counter(1, (0,0)), Counter(2, (5,4)))

def drawGrid():    
    for r in range(ROWS):
        for c in range(COLUMNS):
            center = calculateCounterCenter(r, c, sideOffset, topOffset, bottomOffset)
            pg.draw.circle(screen, EMPTY_COLOUR, center, RADIUS)
            
            if DEBUG: #Draw debug lines to check proper position
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

        counters.update()
        counters.draw(screen)

        clock.tick(FPS)
        pg.display.update()