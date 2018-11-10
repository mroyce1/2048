import numpy as np
import pygame

def move_left(vec):
    score = 0
    changed = False
    prev = vec

    new_vec = [i for i in vec if i != 0]
    new_vec += [0 for i in range(len(vec) - len(new_vec))]
    vec = new_vec

    for i in range(0, 3):
        if(vec[i] == vec[i+1]):
            changed = True
            vec[i] += vec[i]
            score += vec[i]
            vec[i+1] = 0

    new_vec = [i for i in vec if i != 0]
    new_vec += [0 for i in range(len(vec) - len(new_vec))]
    if(new_vec == prev):
        return None
    return (np.array(new_vec), score)



def move_right(vec):
    prev = vec
    score = 0

    changed = False

    new_vec = [i for i in vec if i != 0]
    new_vec = [0 for i in range(len(vec) - len(new_vec))] + new_vec
    vec = new_vec
    
    for i in range(3, 0, -1):
        if(vec[i] == vec[i-1]):
            changed = True
            vec[i] += vec[i]
            score += vec[i]
            vec[i-1] = 0

    new_vec = [i for i in vec if i != 0]
    new_vec = [0 for i in range(len(vec) - len(new_vec))] + new_vec
    if(new_vec == prev):
        return None
    return (np.array(new_vec), score)


def gen_moves():
    arrays = {}
    seq = [0]
    for i in range(1, 14):
        seq.append(2 ** i)
        
    for i in range(13):
        for j in range(13):
            for k in range(13):
                for l in range(13):
                    v = [seq[i], seq[j], seq[k], seq[l]]
                    arrays[seq[i], seq[j], seq[k], seq[l], 'l'] = move_left([seq[i], seq[j], seq[k], seq[l]])
                    arrays[seq[i], seq[j], seq[k], seq[l], 'r'] = move_right([seq[i], seq[j], seq[k], seq[l]])
    return arrays

    
def gen_colors():
    d = {}
    rgb = [(185, 173, 159), (129, 128, 215), (162, 90, 214), (38, 105, 221), (33, 185, 213),
            (0, 202, 155), (67, 207, 23), (247, 192, 1), (245, 129, 20), (255, 84, 61), (255, 20, 145), (255, 20, 59), (255, 20, 59)]
    d[0] = rgb[0]
    for i in range(1, 13):
        d[2 ** i] = rgb[i]
    return d

def gen_coords():
    c = {}
    b = {}
    margin = 2
    x_d = (500-margin)/4
    for i in range(4):
        for j in range(4):
            c[i, j] = [(x_d+margin)*i,
                        (x_d+margin)*j, x_d, x_d]
            b[i, j] = pygame.Rect([(x_d+margin)*i,
                                    (x_d+margin)*j, x_d, x_d])
    return c, b
