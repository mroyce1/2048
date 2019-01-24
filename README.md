# 2048
Clone of the game 2048 written in Python. 
Reinforcement learning is realized with [keras-rl](https://github.com/keras-rl/keras-rl) and the gym environment.
Moves are pre-generated on startup. 
Unfortunately, keras-rl can't really continue training from saved weights (i.e. weights will be loaded but are only available for testing). So I just dump the memory via pickle and then load it again in order to resume training.
