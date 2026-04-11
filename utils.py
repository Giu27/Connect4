from settings import *

sideOffset = int(WIDTH * (SIDE_PADDING / 100))
topOffset = int(HEIGHT * (TOP_PADDING / 100))
bottomOffset = int(HEIGHT * (BOTTOM_PADDING / 100))

def calculateCounterCenter(row, column, sideOffset, topOffset, bottomOffset):
    actualWidth = WIDTH - sideOffset * 2
    actualHeight = HEIGHT - topOffset - bottomOffset
    hStep = (actualWidth - 2 * RADIUS) / (COLUMNS - 1) if COLUMNS > 1 else 0 #Prevents division by 0 if only one column or row
    vStep = (actualHeight - 2 * RADIUS) / (ROWS - 1) if ROWS > 1 else 0
    return (RADIUS + sideOffset + hStep * column , RADIUS + topOffset  + vStep * row)