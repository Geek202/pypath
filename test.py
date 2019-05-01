import pypath
import pygame
import time
from pypath.MapLoader import *

TILESIZE = 16

pygame.init()

mp = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
]

map8 = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 1, 1, 0],
    [0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0]
]

maze1 = [
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0]
]

maze2 = MapLoaderCSV(".\\maze2.csv").getMap()

# maze4 = MapLoaderImage(".\\maze4.png").getMap()

maze5 = MapLoaderCSV(".\\maze5.csv").getMap()

maze6 = MapLoaderCSV(".\\maze6.csv").getMap()

# print(maze2)

WIDTH = 39 * TILESIZE
HEIGHT = 23 * TILESIZE

STARTPOS = (0, 0)
ENDPOS = (22, 39)

pathfinder = pypath.PathFindingMap(maze5, (23, 39))

dsp = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver!")

pygame.display.toggle_fullscreen()

dsp.fill((255, 0, 0))
pygame.display.update()


def pos_callback(pos):
    global dsp
    rct = pygame.Rect(pos[0] * TILESIZE, pos[1] * TILESIZE, TILESIZE, TILESIZE)
    '''dsp.fill((0, 0, 0), rct)
    pygame.display.update(rct)
    time.sleep(0.0125)'''
    dsp.fill((0, 255, 0), rct)
    pygame.display.update(rct)
    time.sleep(.0125)
    print("DEBUG: POS SCAN")


def solid_pos_callback(pos):
    global dsp
    rct = pygame.Rect(pos[0] * TILESIZE, pos[1] * TILESIZE, TILESIZE, TILESIZE)
    '''dsp.fill((0, 0, 0), rct)
    pygame.display.update(rct)
    time.sleep(0.0125)'''
    dsp.fill((255, 0, 0), rct)
    pygame.display.update(rct)
    time.sleep(.0125)
    print("DEBUG: SOLID POS SCAN")


def path_update_callback(pos):
    global dsp
    rct = pygame.Rect(pos[0] * TILESIZE, pos[1] * TILESIZE, TILESIZE, TILESIZE)
    dsp.fill((0, 0, 255), rct)
    pygame.display.update(rct)
    time.sleep(.0125)
    print("DEBUG: ROUTE UPDATE")


starttime = time.time()
path = pathfinder.findpath(STARTPOS, ENDPOS, solid_pos_callback=solid_pos_callback,
                           pos_callback=pos_callback,
                           path_update_callback=path_update_callback)
endtime = time.time()

print("Pathing complete: Path found!\nTook:\n{0} s".format(endtime - starttime))
print(path)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            running = False
    pygame.display.update()
pygame.quit()
