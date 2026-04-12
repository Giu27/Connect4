import math
from settings import *

sideOffset = int(WIDTH * (SIDE_PADDING / 100))
topOffset = int(HEIGHT * (TOP_PADDING / 100))
bottomOffset = int(HEIGHT * (BOTTOM_PADDING / 100))

def calculateCounterCenter(row : int, column : int, sideOffset : int = sideOffset, topOffset : int = topOffset, bottomOffset : int = bottomOffset):
    """Given the row and column (plus the offsets), returns the counter's center"""
    actualWidth = WIDTH - sideOffset * 2
    actualHeight = HEIGHT - topOffset - bottomOffset
    hStep = (actualWidth - 2 * RADIUS) / (COLUMNS - 1) if COLUMNS > 1 else 0 #Prevents division by 0 if only one column or row
    vStep = (actualHeight - 2 * RADIUS) / (ROWS - 1) if ROWS > 1 else 0
    return (RADIUS + sideOffset + hStep * column , RADIUS + topOffset  + vStep * row)

def getColumn(mouse_x : int, sideOffset : int = sideOffset):
    """Given the mouse cursor x coordinate (and the offset), returns the column"""
    if mouse_x <= sideOffset:
        return 0
    if mouse_x >= WIDTH - sideOffset:
        return COLUMNS - 1
    actualWidth = WIDTH + (-sideOffset + RADIUS) * 2
    hStep = actualWidth / COLUMNS
    return int(math.floor((mouse_x - sideOffset + RADIUS) // hStep))