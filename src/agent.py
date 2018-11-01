from copy import deepcopy
import random
import math
from time import time

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
            d[i] = self.descend(state_copy, 0)
        print(d)
        return max(d, key=d.get)

    def descend(self, state, depth):
        val = 0
        if(depth == 3):
            if(not state.move_possible()):
                return -10000
            return state.free_tiles/depth
        for i in range(4):
            state_copy = deepcopy(state)
            state_copy.move_cells(range(4)[i])
            if(state.moves_performed == state_copy.moves_performed):
                continue
            val += self.descend(state_copy, depth+1)
        return val

    def __str__(self):
        return self.name
