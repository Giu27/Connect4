import pygame as pg
import sys
from settings import *
from utils import *

pg.init()

class Counter(pg.sprite.Sprite):
    def __init__(self, player : int, gridPos : tuple[int, int]):
        super().__init__()
        self.image = pg.Surface((RADIUS * 2, RADIUS * 2), pg.SRCALPHA, 32)
        colour = PLAYER1_BORDER_COLOUR if player == 1 else PLAYER2_BORDER_COLOUR
        pg.draw.circle(self.image, colour, (RADIUS, RADIUS), RADIUS)

        inner_colour = PLAYER1_INNER_COLOUR if player == 1 else PLAYER2_INNER_COLOUR
        inner_radius = RADIUS * (1 - BORDER_PERCENTAGE / 100)
        pg.draw.circle(self.image, inner_colour, (RADIUS, RADIUS), inner_radius)

        self.target = calculateCounterCenter(gridPos[0], gridPos[1])

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

currentPlayer = 1
grid = [[0 for column in range(COLUMNS)] for row in range(ROWS)] #Will be used by the actual logic of the game
getRow = [ROWS - 1 for column in range(COLUMNS)]
counters = pg.sprite.Group()
win = False

def reset():
    """Resets game to initial state"""
    global grid, currentPlayer, getRow, win
    grid = [[0 for column in range(COLUMNS)] for row in range(ROWS)]
    getRow = [ROWS - 1 for column in range(COLUMNS)]
    counters.empty()
    currentPlayer = 1
    win = False

def drawGrid():
    """Draws the holes for the counters"""    
    for r in range(ROWS):
        for c in range(COLUMNS):
            center = calculateCounterCenter(r, c)
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

def check(player : int, gridPos : tuple[int, int], move : tuple[int, int]) -> int:
    counters = 1
    for i in range(1, COUNTERS_TO_WIN): 
        if grid[gridPos[0] + move[0] * i][gridPos[1] + move[1] * i] != player:
            counters = 1
            break
        else:
            counters += 1
            if counters == COUNTERS_TO_WIN: break
    return counters

def checkWin(player : int, gridPos : tuple[int, int]) -> bool:
    """Given a player and the last counter placed by that player, returns true if the player won"""
    counters = 1
    if gridPos[0] <= ROWS - COUNTERS_TO_WIN: #Check vertical win
        counters = check(player, gridPos, (1, 0))

    if gridPos[1] <= COLUMNS - COUNTERS_TO_WIN and counters != COUNTERS_TO_WIN:
        if gridPos[0] <= ROWS - COUNTERS_TO_WIN: #Check right diagonal win.
            counters = check(player, gridPos, (1, 1))
        if counters != COUNTERS_TO_WIN: #check right horizontal
            counters = check(player, gridPos, (0, 1))
    
    if gridPos[1] >= 0 + COUNTERS_TO_WIN and counters != COUNTERS_TO_WIN:
        if gridPos[0] <= ROWS - COUNTERS_TO_WIN: #Check left diagonal win.
            counters = check(player, gridPos, (1, -1))
        if counters != COUNTERS_TO_WIN: #check left horizontal
            counters = check(player, gridPos, (0, -1))

    if counters == COUNTERS_TO_WIN:
        return True
    else: 
        return False

if __name__ == "__main__":
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    DEBUG = not DEBUG
                if event.key == pg.K_r:
                    reset()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if win:
                        print("Press R to reset!")
                    else:
                        if len(counters.sprites()) == 0: ready = True
                        elif counters.sprites()[-1].placed: ready = True
                        else: ready = False
                        if ready:
                            chosenColumn = getColumn(event.pos[0])
                            availableRow = getRow[chosenColumn]
                            if availableRow >= 0:
                                counters.add(Counter(currentPlayer, (availableRow,chosenColumn)))
                                grid[availableRow][chosenColumn] = currentPlayer
                                win = checkWin(currentPlayer, (availableRow, chosenColumn))

                                if not win:
                                    currentPlayer = 2 if currentPlayer == 1 else 1
                                    getRow[chosenColumn] -= 1
        if win and counters.sprites()[-1].placed:
            print(f"{currentPlayer} won!")

        screen.fill(BACKGROUND_COLOUR)

        drawGrid()

        counters.update()
        counters.draw(screen)

        if DEBUG:
            for sprite in counters:
                pg.draw.rect(screen,"purple",sprite.rect,2)

            print(f"FPS: {int(clock.get_fps())}")
            print(f"Current Player: {currentPlayer}")
            print(f"Counters count: {len(counters.sprites())}")

        clock.tick(FPS)
        pg.display.update()