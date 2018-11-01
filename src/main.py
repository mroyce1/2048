import pygame
import random
import math
from domain import Grid, Cell
from agent import SimpleAgent
import sys

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 30)
screen_size = [500, 500]
margin = 2
grid = Grid(screen_size, margin)
# print(grid)
screen = pygame.display.set_mode(screen_size)
score = 0


def encode_one_hot(state):
    d = {}
    # for i, x in enumerate(state.cells):
    #     for j, c in enumerate(x):
    #         d[str(''.join([str(i), str(j)]))] = '{0:016b}'.format(c.val)
    # df = pd.DataFrame(d)

    l = []
    highest_cell = math.log(state.get_highest_cell(), 2)
    for i, x in enumerate(state.cells):
        for j, c in enumerate(x):
            if(c.val > 0):
                d[str(''.join([str(i), str(j)]))] = math.log(
                    c.val, 2)/highest_cell
                l.append(math.log(c.val, 2)/highest_cell)
            else:
                d[str(''.join([str(i), str(j)]))] = 0
                l.append(0)
    print(l)
    return l


encoded = encode_one_hot(grid)

ag = SimpleAgent('mcts')
while(True):
    events = pygame.event.get()
    for e in events:
        if (e.type == pygame.KEYDOWN):
            if (e.key == pygame.K_LEFT):
                grid.move_cells(3)
            if (e.key == pygame.K_RIGHT):
                grid.move_cells(1)
            if (e.key == pygame.K_UP):
                grid.move_cells(0)
            if (e.key == pygame.K_DOWN):
                grid.move_cells(2)
            if (e.key == pygame.K_q):
                print("Exiting...")
                sys.exit(0)
            if (e.key == pygame.K_r):
                print("Reset")
                grid = Grid(screen_size, margin)
            print("score: ", grid.score)
        if e.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            grid.check_click(*pos)
    agent_choice = ag.get_move(grid)
    print("score: ", grid.score)
    res = grid.move_cells(range(4)[agent_choice])
    grid.draw(screen, myfont)
    pygame.display.update()
    if(not res):
        print("Game Over!")
        print(grid)
        input()
        grid = Grid(screen_size, margin)
