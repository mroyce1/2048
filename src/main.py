import pygame
import random
import math
from domain import Grid
from agent import SimpleAgent
import sys

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 30)
screen_size = [500, 500]
margin = 2
grid = Grid(screen_size, margin)

screen = pygame.display.set_mode(screen_size)


ag = SimpleAgent('mcts')
while(True):
    res = True
    events = pygame.event.get()
    for e in events:
        if (e.type == pygame.KEYDOWN):
            if (e.key == pygame.K_LEFT):
                res = grid.move_cells(3)
            if (e.key == pygame.K_RIGHT):
                res = grid.move_cells(1)
            if (e.key == pygame.K_UP):
                res = grid.move_cells(0)
            if (e.key == pygame.K_DOWN):
                res = grid.move_cells(2)
            if (e.key == pygame.K_q):
                print("Exiting...")
                sys.exit(0)
            if (e.key == pygame.K_r):
                print("Reset")
                grid.reset()
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
