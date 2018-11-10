from copy import deepcopy
import numpy as np
import random


class SimpleAgent(object):
    def __init__(self, name):
        self.name = name
        self.prev_state = None

    def get_move(self, state):
        d = {}
        for i in range(4):
            state_copy = deepcopy(state)
            state_copy.move_cells(range(4)[i])
            if(state_copy.moves_performed == state.moves_performed):
                continue
            d[i] = self.descend2(state_copy, 1)
        # print(d)
        return max(d, key=d.get)

    def descend(self, state, depth):
        val = 0
        if(depth == 7):
            # if(not state.move_possible()):
            #     return -10000
            return state.free_tiles/depth
        for i in range(4):
            state_copy = deepcopy(state)
            state_copy.move_cells(range(4)[i])
            if(state.moves_performed == state_copy.moves_performed):
                continue
            val += (self.descend(state_copy, depth+1)/depth)
            # val += self.descend(state_copy, depth+1)
        return val

    def __str__(self):
        return self.name

    def descend2(self, state, depth):
        # if(depth == 4):
        if(depth >= int((15-state.free_tiles)/3)):
            return state.score/depth
            if(not state.move_possible()):
                return -10000
            # return state.free_tiles/depth
        val = 0
        for i in range(4):
            state_copy = deepcopy(state)
            state_copy.move_cells(range(4)[i])
            if(state.moves_performed == state_copy.moves_performed):
                continue
            # zeros = np.asarray(np.where(state_copy.cells == 0)).T.tolist()
            zeros = np.where(state_copy.cells == 0)
            for x in range(len(zeros[0])):
                i = zeros[0][x]
                j = zeros[1][x]
                state_copy2 = deepcopy(state_copy)
                state_copy2.cells[i][j] = 4
                state_copy2.free_tiles -= 1
                val += 0.1 * self.descend2(state_copy2, depth+1)
                state_copy3 = deepcopy(state_copy)
                state_copy3.cells[i][j] = 2
                state_copy3.free_tiles -= 1
                val += 0.9 * self.descend2(state_copy3, depth+1)
                # val += self.descend2(state_copy3, depth+1)/(depth)
        return val/depth

    def __str__(self):
        return self.name
