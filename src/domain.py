import pygame
import math
import random
from copy import deepcopy



class Grid(object):
    def __init__(self, screen_size, margin):
        self.margin = margin
        self.screen_size = screen_size
        self.cells = []
        self.x_d = (screen_size[0]-margin)/4
        self.y_d = (screen_size[1]-margin)/4
        self.score = 0
        self.free_tiles = 16
        self.moves_performed = 0
        for i in range(4):
            self.cells.append([])
            for j in range(4):
                self.cells[i].append(
                    Cell(0, [i, j], self.x_d, self.y_d, margin))
        for i in range(4):
            self.spawn_random_cell()

    def spawn_random_cell(self):
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        while(self.cells[x][y].val != 0):
            x = random.randint(0, 3)
            y = random.randint(0, 3)
        self.cells[x][y].val = 4 if (random.randint(0, 9) == 0) else 2
        self.cells[x][y].set_col()
        self.free_tiles -= 1

    def __str__(self):
        out = ''
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                out += str(self.cells[i][j]) + ' '
            out += '\n'
        return out

    def draw(self, screen, font):
        for x in self.cells:
            for y in x:
                y.draw(screen, font)

    def move_cells(self, direction):
        moved = 0
        for _ in range(4):
            if(direction == 'UP'):
                for x in range(4):
                    moved += self.cells[0][x].move_up(
                        self.cells, self.increment_score)
            if(direction == 'DOWN'):
                for x in range(4):
                    moved += self.cells[3][x].move_down(
                        self.cells, self.increment_score)
            if(direction == 'LEFT'):
                for x in range(4):
                    moved += self.cells[x][0].move_left(
                        self.cells, self.increment_score)
            if(direction == 'RIGHT'):
                for x in range(4):
                    moved += self.cells[x][3].move_right(
                        self.cells, self.increment_score)

        self.reset_merged()
        if moved > 0:
            self.spawn_random_cell()
            self.moves_performed += 1
        # print("free tiles: ", self.free_tiles)
        return self.move_possible()

    def increment_score(self, n):
        self.score += n
        self.free_tiles += 1

    def get_highest_cell(self):
        return max([i.val for x in self.cells for i in x])

    def check_click(self, x, y):
        for row in self.cells:
            for c in row:
                if(c.click_is_inside(x, y)):
                    print(c)
                    return

    def reset_merged(self):
        for c in [i for x in self.cells for i in x]:
            c.merged = False

    def move_possible(self):
        if(0 in [i.val for x in self.cells for i in x]):
            return True
        for i in range(len(self.cells)):
            for j in range(len(self.cells[0])-1):
                if(self.cells[i][j].val == self.cells[i][j+1].val):
                    return True
                if(self.cells[j][i].val == self.cells[j+1][i].val):
                    return True
                if(self.cells[i][j].val == self.cells[i][j+1].val):
                    return True
                if(self.cells[j][i].val == self.cells[j+1][i].val):
                    return True
        return False


class Cell(object):
    def __init__(self, val, pos, x_d, y_d, margin):
        self.val = val
        self.set_col()
        self.pos = pos
        self.coords = [(x_d+margin)*self.pos[1],
                       (y_d+margin)*self.pos[0], x_d, y_d]
        self.box = pygame.Rect(self.coords)
        self.merged = False

    def update_val(self, n):
        self.val = n
        self.set_col()

    def move_up(self, cells, score):
        moved = 0
        if(self.pos[0] > 0):
            tmp = cells[self.pos[0]-1][self.pos[1]]
            if(tmp.val == 0 and self.val != 0):
                tmp.update_val(self.val)
                self.update_val(0)
                moved += 1
            elif(tmp.val == self.val and self.val != 0 and not tmp.merged and not self.merged):
                tmp.update_val(tmp.val + self.val)
                self.update_val(0)
                score(tmp.val)
                self.merged = True
                tmp.merged = True
                moved += 1
        if(self.pos[0] < 3):
            moved += cells[self.pos[0]+1][self.pos[1]].move_up(cells, score)
        return moved

    def move_down(self, cells, score):
        moved = 0
        if(self.pos[0] < 3):
            tmp = cells[self.pos[0]+1][self.pos[1]]
            if(tmp.val == 0 and self.val != 0):
                tmp.update_val(self.val)
                self.update_val(0)
                moved += 1
            elif(tmp.val == self.val and self.val != 0 and not tmp.merged and not self.merged):
                tmp.update_val(tmp.val + self.val)
                self.update_val(0)
                self.merged = True
                tmp.merged = True
                score(tmp.val)
                moved += 1
        if(self.pos[0] > 0):
            moved += cells[self.pos[0]-1][self.pos[1]].move_down(cells, score)
        return moved

    def move_left(self, cells, score):
        moved = 0
        if(self.pos[1] > 0):
            tmp = cells[self.pos[0]][self.pos[1]-1]
            if(tmp.val == 0 and self.val != 0):
                tmp.update_val(self.val)
                self.update_val(0)
                moved += 1
            elif(tmp.val == self.val and self.val != 0 and not tmp.merged and not self.merged):
                tmp.update_val(tmp.val + self.val)
                self.update_val(0)
                self.merged = True
                tmp.merged = True
                score(tmp.val)
                moved += 1
        if(self.pos[1] < 3):
            moved += cells[self.pos[0]][self.pos[1]+1].move_left(cells, score)
        return moved

    def move_right(self, cells, score):
        moved = 0
        if(self.pos[1] < 3):
            tmp = cells[self.pos[0]][self.pos[1]+1]
            if(tmp.val == 0 and self.val != 0):
                tmp.update_val(self.val)
                self.update_val(0)
                moved += 1
            elif(tmp.val == self.val and self.val != 0 and not tmp.merged and not self.merged):
                tmp.update_val(tmp.val + self.val)
                self.update_val(0)
                self.merged = True
                tmp.merged = True
                score(tmp.val)
                moved += 1
        if(self.pos[1] > 0):
            moved += cells[self.pos[0]][self.pos[1]-1].move_right(cells, score)
        return moved

    def set_col(self):
        k = 0
        x = self.val
        while(x >= 2):
            x /= 2
            k += 1
        self.col = [(185, 173, 159), (129, 128, 215), (162, 90, 214), (38, 105, 221), (33, 185, 213),
                    (0, 202, 155), (67, 207, 23), (247, 192, 1), (245, 129, 20), (255, 84, 61), (255, 20, 145), (255, 20, 59), (255, 20, 59)][k]

    def click_is_inside(self, x, y):
        if(x < self.coords[0]):
            return False
        if(y < self.coords[1]):
            return False
        return x < self.coords[0]+self.coords[2] and y < self.coords[1] + self.coords[3]

    def __str__(self):
        return ''.join([str(self.pos), ': ', str(self.val)])

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.col, self.box)
        text_surface = font.render(str(self.val), False, (0, 0, 0))
        screen.blit(text_surface, self.coords)
