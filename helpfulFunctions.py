
##############################################
#intended to create a set of helpful functions for testing purposes
#And for conciseness
##############################################
import math, sys
import numpy as np
# Obtained from class notes
def findInstallLibrary(library):
    print(f'"{sys.executable}" -m pip install '+library)

def make2dList(rows, cols):
    return [ ([None] * cols) for row in range(rows) ]

# Helper function for print2dList.
# This finds the maximum length of the string
# representation of any item in the 2d list
def maxItemLength(a):
    maxLen = 0
    for row in range(len(a)):
        for col in range(len(a[row])):
            maxLen = max(maxLen, len(repr(a[row][col])))
    return maxLen

def print2dList(a):
    if a == []:
        print([])
        return
    print()
    rows, cols = len(a), len(a[0])
    maxCols = max([len(row) for row in a])
    fieldWidth = max(maxItemLength(a), len(f'col={maxCols-1}'))
    rowLabelSize = 5 + len(str(rows-1))
    rowPrefix = ' '*rowLabelSize+' '
    rowSeparator = rowPrefix + '|' + ('-'*(fieldWidth+3) + '|')*maxCols
    print(rowPrefix, end='  ')
    # Prints the column labels centered
    for col in range(maxCols):
        print(f'col={col}'.center(fieldWidth+2), end='  ')
    print('\n' + rowSeparator)
    for row in range(rows):
        # Prints the row labels
        print(f'row={row}'.center(rowLabelSize), end=' | ')
        # Prints each item of the row flushed-right but the same width
        for col in range(len(a[row])):
            print(repr(a[row][col]).center(fieldWidth+1), end=' | ')
        # Prints out missing cells in each column in case the list is ragged
        missingCellChar = chr(10006)
        for col in range(len(a[row]), maxCols):
            print(missingCellChar*(fieldWidth+1), end=' | ')
        print('\n' + rowSeparator)
    print()



#Self-coded
def distance(x0, y0, x1, y1):
    return(math.sqrt((x0-x1)**2 + (y0-y1)**2))

#Takes two tuples of four elements each and returns if the rectangles made
#By the tuples of coordinates intersect
def rectangleIntersect(rect1Dim, rect2Dim):
    rect1x0, rect1y0, rect1x1, rect1y1 = rect1Dim
    rect2x0, rect2y0, rect2x1, rect2y1 = rect2Dim
    rect1xR = max(rect1x0, rect1x1)
    rect1xL = min(rect1x0, rect1x1)
    rect1yT = min(rect1y0, rect1y1)
    rect1yB = max(rect1y0, rect1y1)
    rect2xR = max(rect2x0, rect2x1)
    rect2xL = min(rect2x0, rect2x1)
    rect2yT = min(rect2y0, rect2y1)
    rect2yB = max(rect2y0, rect2y1)
    if rect1xR <= rect2xL or rect2xR <= rect1xL:
        return False
    if rect1yB <= rect2yT or rect2yB <= rect1yT:
        return False
    return True


def linefit(xCoords, yCoords):
    x0, x1 = xCoords
    y0, y1 = yCoords
    try:
        slope = (y1 - y0)/(x1 - x0)
    except:
        slope = 0

    constant = y1 - slope * x1
    return(slope, constant)
#Takes three tuples, lineStart and lineEnd are (x, y) coordinates, rectDim has four elements
def lineInRectangle(lineStart, lineEnd, rectDim):
    rectx0, recty0, rectx1, recty1 = rectDim
    xCoords = (lineStart[0], lineEnd[0])
    yCoords = (lineStart[1], lineEnd[1]) #bound lines
    coefficients = linefit(xCoords, yCoords)
    inXRegion = False
    inYRegion = False
    for x in (rectx0, rectx1):
        if min(lineStart[0], lineEnd[0]) <= x <= max(lineStart[0], lineEnd[0]):
            inXRegion = True
    for y in (recty0, recty1):
        if min(lineStart[1], lineEnd[1]) <= y <= max(lineStart[1], lineEnd[1]):
            inYRegion = True
    if not (inXRegion or inYRegion):
        return False
    if rectx0 * coefficients[0] + coefficients[1] > recty0:
        checker = 1
    else:
        checker = -1

    for x, y in [(rectx0, recty1), (rectx1, recty1), (rectx1, recty0)]:
        if x * coefficients[0] + coefficients[1] < y and checker == 1:
            return True
        if x * coefficients[0] + coefficients[1] > y and checker == -1:
            return True
    return False

def pointInRectangle(pointCoords, rectCoords):
    rectx0, recty0, rectx1, recty1 = rectCoords
    rectxR = max(rectx0, rectx1)
    rectxL = min(rectx0, rectx1)
    rectyB = max(recty0, recty1)
    rectyT = min(recty0, recty1)
    if rectxR < pointCoords[0] or rectxL > pointCoords[0]:
        return False
    if rectyB < pointCoords[1] or rectyT > pointCoords[1]:
        return False
    return True

def midpoint(n1, n2):
    return ((n1 + n2)/2)

def thunk():
    return(False)

