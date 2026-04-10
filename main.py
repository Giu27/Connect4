import pygame as pg
import sys
from settings import *

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT), 0, 32)
pg.display.set_caption("Connect 4!")

clock = pg.Clock()

while True:
    screen.fill(BACKGROUND_COLOR)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    clock.tick(FPS)
    pg.display.update()