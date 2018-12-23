import pygame
import math
import random
import pickle
from datetime import datetime
from copy import deepcopy
import numpy as np
from generate import gen_moves, gen_coords, gen_colors
import gym
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy, BoltzmannQPolicy, LinearAnnealedPolicy
from rl.memory import SequentialMemory
import numpy as np
import pandas as pd






class Grid(gym.Env):
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
        self.prev_moves = []
        self.reset()

    def reset(self):
        self.cells = []
        self.score = 0
        self.free_tiles = 16
        self.moves_performed = 0
        self.cells = np.zeros(shape=(4, 4))
        for _ in range(4):
            self.spawn_random_cell()
        # return self.cells
        return self.normalize_grid()

    def step(self, action):
        old_score = self.score
        prev_moves = self.moves_performed
        self.move_cells(action)
        # s = self.score - old_score
        s = self.free_tiles/16
        # if len(self.prev_moves) >= 5:
        #     self.prev_moves = self.prev_moves[:4]
        if self.moves_performed == prev_moves:
            # self.prev_moves = [0] + self.prev_moves
            # print('invalid move')
            s = -0.3
        # else:
        #     self.prev_moves = [1] + self.prev_moves
        # if sum(self.prev_moves) == 0:
            # self.move_cells((action+1)%4)
            # return self.step((action+1)%4)
        done = bool(not self.move_possible())
        # if(done):
        #     s = -1
        # return self.cells, s, done, {}
        return self.normalize_grid(), s, done, {}


    

        # state_copy = deepcopy(self)
        # state_copy.move_cells(range(4)[action])
        # return state_copy, state_copy.score, self.move_possible(), {}

    def spawn_random_cell(self):
        zeros = np.where(self.cells == 0)
        assert len(zeros[0]) > 0, 'No zero tiles to spawn a cell > 0.'

        rdm = random.randint(0, len(zeros[0])-1)
        self.cells[zeros[0][rdm]][zeros[1][rdm]] = 4 if (
            random.randint(0, 9) == 0) else 2
        self.free_tiles -= 1

    def __str__(self):
        out = ''
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                out += str(self.cells[i][j]) + ' '
            out += '\n'
        return out

    def normalize_grid(self):
        x = self.cells.copy()
        # return (x[np.where(x > 0) = math.log(x, 2)])
        # np.place(x, x > 0.0, math.log(x, 2))

        #pick log2(4096) = 12 as normalizing constant
        max_val = 12.0
        # max_val = math.log(np.amax(self.cells), 2)

        non_zeros = np.where(self.cells != 0)
        for i in range(len(non_zeros[0])):
            x[non_zeros[0][i]][non_zeros[1][i]] = math.log(self.cells[non_zeros[0][i]][non_zeros[1][i]], 2)/max_val
        # print('normalized')
        # print(x)
        # input()
        return x

    def render(self, mode='human', close=False):
        self.draw(screen, myfont)
        pygame.display.update()
        input()

    def draw(self, screen, font):
        for i in range(len(self.cells)):
            for j in range(len(self.cells)):
                pygame.draw.rect(
                    screen, Grid.colors[self.cells[i, j]], Grid.boxes[i, j])
                col = (0, 0, 0)
                val = self.cells[i, j]
                # if val > 4:
                #     col = (255, 255, 255)
                text_surface = font.render(
                    str(int(val)), False, col)
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
            zeros = np.where(self.cells == 0)
            self.free_tiles = len(zeros[0])
            # unique, counts = np.unique(self.cells, return_counts=True)
            # if(unique[0] == 0):
            #     self.free_tiles = counts[0]
            # else:
            #     self.free_tiles = 0
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


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 30, bold=True)
screen_size = [500, 500]
margin = 2
grid = Grid(screen_size, margin)

screen = pygame.display.set_mode(screen_size)


font = pygame.font.SysFont('Arial', 30)
env = Grid(screen_size, 2)