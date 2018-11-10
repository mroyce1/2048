import pygame
import math
import random
from copy import deepcopy
import numpy as np
from generate import gen_moves, gen_coords, gen_colors


class Grid(object):
    pre_moves = gen_moves()
    coords, boxes = gen_coords()
    colors = gen_colors()

    def __init__(self, screen_size=None, margin=None):
        if(margin == None):
            return
        self.margin = margin
        self.screen_size = screen_size
        self.x_d = (screen_size[0]-margin)/4
        self.y_d = (screen_size[1]-margin)/4
        self.reset()

    def reset(self):
        self.cells = []
        self.score = 0
        self.free_tiles = 16
        self.moves_performed = 0
        self.cells = np.zeros(shape=(4, 4))
        for _ in range(4):
            self.spawn_random_cell()

    def step(self, action):
        state_copy = deepcopy(self)
        state_copy.move_cells(range(4)[action])
        return state_copy, state_copy.score, self.move_possible(), {}

    def spawn_random_cell(self):
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        while(self.cells[y][x] != 0):
            x = random.randint(0, 3)
            y = random.randint(0, 3)
        self.cells[y][x] = 4 if (random.randint(0, 9) == 0) else 2
        self.free_tiles -= 1

    def __str__(self):
        out = ''
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                out += str(self.cells[i][j]) + ' '
            out += '\n'
        return out

    def draw(self, screen, font):
        for i in range(len(self.cells)):
            for j in range(len(self.cells)):
                pygame.draw.rect(
                    screen, Grid.colors[self.cells[i, j]], Grid.boxes[i, j])
                text_surface = font.render(
                    str(int(self.cells[i, j])), False, (0, 0, 0))
                screen.blit(text_surface, Grid.coords[i, j])


    def move_cells(self, direction):
        moved = False
        score = 0
        if(direction == 0):
            for i in range(4):
                tmp = Grid.pre_moves[self.cells[i, 0], self.cells[i,
                                                                  1], self.cells[i, 2], self.cells[i, 3], 'l']
                if(tmp is None):
                    continue
                moved = True
                self.cells[i, :] = tmp[0]
                score += tmp[1]
        if(direction == 2):
            for i in range(4):
                tmp = Grid.pre_moves[self.cells[i, 0], self.cells[i,
                                                                  1], self.cells[i, 2], self.cells[i, 3], 'r']
                if(tmp is None):
                    continue
                moved = True
                score += tmp[1]
                self.cells[i, :] = tmp[0]
        if(direction == 3):
            for i in range(4):
                tmp = Grid.pre_moves[self.cells[0, i], self.cells[1,
                                                                  i], self.cells[2, i], self.cells[3, i], 'l']
                if(tmp is None):
                    continue
                moved = True
                score += tmp[1]
                self.cells[:, i] = tmp[0]
        if(direction == 1):
            for i in range(4):
                tmp = Grid.pre_moves[self.cells[0, i], self.cells[1,
                                                                  i], self.cells[2, i], self.cells[3, i], 'r']
                if(tmp is None):
                    continue
                moved = True
                score += tmp[1]
                self.cells[:, i] = tmp[0]

        if moved:
            self.score += score
            self.spawn_random_cell()
            self.moves_performed += 1
            unique, counts = np.unique(self.cells, return_counts=True)
            if(unique[0] == 0):
                self.free_tiles = counts[0]
            else:
                self.free_tiles = 0
        return self.move_possible()

    def check_click(self, x, y):
        for k, v in Grid.coords.items():
            if(x < v[0] or y < v[1]):
                continue
            if(x >= v[0]+v[2] or y >= v[1] + v[3]):
                continue
            print(k)
            return

    def move_possible(self):
        if(self.free_tiles > 0):
            return True

        for i in range(len(self.cells)):
            for j in range(len(self.cells)-1):
                if self.cells[i][j] == self.cells[i][j+1]:
                    return True
                if(self.cells[j][i] == self.cells[j+1][i]):
                    return True
                if(self.cells[i][j] == self.cells[i][j+1]):
                    return True
                if(self.cells[j][i] == self.cells[j+1][i]):
                    return True
        return False

    def __deepcopy__(self, memodict={}):
        new_grid = Grid()
        new_grid.free_tiles = self.free_tiles
        new_grid.moves_performed = self.moves_performed
        new_grid.score = self.score
        new_grid.cells = np.copy(self.cells)
        return new_grid