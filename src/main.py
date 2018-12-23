import pygame
import random
import math
import pickle
from datetime import datetime
from domain import Grid
from agent import ExpectimaxAgent
import sys
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy, BoltzmannQPolicy, LinearAnnealedPolicy
from rl.memory import SequentialMemory
import numpy as np
import pandas as pd



pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 30, bold=True)
screen_size = [500, 500]
margin = 2
grid = Grid(screen_size, margin)

screen = pygame.display.set_mode(screen_size)


screen = pygame.display.set_mode(screen_size)
font = pygame.font.SysFont('Arial', 30)
env = Grid(screen_size, 2)

nb_actions = 4
nb_steps = int(2e6)
nb_steps_annealed = int(1.25e6)
nb_steps_warmup = int(0.25e6)
window_length = 1
nb_hidden = 256
memory_size = int(2e6)
print("memory_size", memory_size)
batch_size = 256
delta_clip = 1.0
train_interval = 100


model = Sequential([
    Flatten(input_shape=(window_length, 4, 4)),
    Dense(nb_hidden),
    Activation("relu"),
    Dense(nb_hidden),
    Activation("relu"),
    Dense(nb_actions),
    Activation("linear")
])
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
print(model.summary())


model = Sequential()
model.add(Flatten(input_shape=(1, 4, 4)))
# model.add(Dense(nb_hidden))
# model.add(Activation('relu'))
model.add(Dense(10))
model.add(Activation('relu'))
model.add(Dense(nb_actions, activation='linear'))
# model.add(Dense(4, activation="softmax"))
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
print(model.summary())

nb_actions = 4
nb_steps = int(2e6)
nb_steps_annealed = int(1.25e6)
nb_steps_warmup = int(0.25e6)
window_length = 1
nb_hidden = 32
memory_size = int(2e6)
print("memory_size", memory_size)
batch_size = 32
delta_clip = 1.0
train_interval = 100

model = Sequential([
    Flatten(input_shape=(window_length, 4, 4)),
    Dense(nb_hidden),
    Activation("relu"),
    Dense(nb_actions),
    Activation("linear")
])
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
print(model.summary())


def train():
    memory = SequentialMemory(limit=50000, window_length=1)
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(
    ), attr='eps', value_max=0.05, value_min=.05, value_test=.01, nb_steps=5000)
    dqn = DQNAgent(model=model, nb_actions=nb_actions, batch_size=batch_size, memory=memory, nb_steps_warmup=1000,
                target_model_update=1e-2, policy=policy)
    dqn.compile(Adam(), metrics=['mae'])
    dqn.fit(env, nb_steps=1000000, visualize=False, verbose=1)
    memfile = datetime.now().time()
    dqn.save_weights(f'saved/dqn_{memfile}.h5f', overwrite=True)
    mem = (memory, memory.actions,
    memory.rewards,
    memory.terminals,
    memory.observations)
    pickle.dump(mem, open(f'saved/memory{memfile}.pickle', "wb"), protocol=-1) # highest protocol means binary format




def test():
    try:
        (memory, memory.actions,
        memory.rewards,
        memory.terminals,
        memory.observations) = pickle.load(open('saved/memoryfile-32-12-7.25mio.pickle', "rb"))
    except:
        print("no memory file found.")
    
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(
    ), attr='eps', value_max=0.05, value_min=.05, value_test=.01, nb_steps=5000)
    dqn = DQNAgent(model=model, nb_actions=nb_actions, batch_size=batch_size, memory=memory, nb_steps_warmup=1000,
                target_model_update=1e-2, policy=policy)
    dqn.compile(Adam(), metrics=['mae'])
    dqn.load_weights('saved/dqn_7.25mio.h5f')
    dqn.test(env, nb_episodes=5, visualize=True)


test()