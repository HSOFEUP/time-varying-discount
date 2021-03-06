import gym
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

import gridworld
from baselines import deepq
from baselines.common import models
from pycolab import rendering


dirs = "../logs/maze2/gamma08/1/maze.pkl"

def rgb_rescale(v):
    return v/255


COLOUR_FG = {' ': tuple([rgb_rescale(v) for v in (123, 132, 150)]), # Background
             '$': tuple([rgb_rescale(v) for v in (214, 182, 79)]),  # Coins
             '@': tuple([rgb_rescale(v) for v in (66, 6, 13)]),     # Poison
             '#': tuple([rgb_rescale(v) for v in (119, 107, 122)]), # Walls of the maze
             'P': tuple([rgb_rescale(v) for v in (153, 85, 74)])}   # Player


def converter(obs):
    converter = rendering.ObservationToArray(COLOUR_FG, permute=(0,1,2))
    converted = np.swapaxes(converter(obs), 1, 2).T
    return converted


def main():
    env = gym.make("sparse-v0")
    act = deepq.learn(
                    env, 
                    network=models.mlp(num_layers=2, num_hidden=128, activation=tf.nn.relu),
                    total_timesteps=0,
                    load_path=dirs)
    
    while True:
        obs, screen_obs = env.reset_with_render()
        done = False
        episode_rew = 0
        converted = converter(screen_obs)
        my_plot = plt.imshow(converted)
        while not done:
            obs, rew, done, _ , screen_obs = env.step_with_render(act(obs)[0])
            #obs, rew, done, _ , screen_obs = env.step_with_render(env.action_space.sample())
            converted = converter(screen_obs)
            plt.ion()
            my_plot.autoscale()
            my_plot.set_data(converted)
            plt.pause(.1)
            plt.draw()
            plt.show()
            print("action: ", act(obs)[0])
            episode_rew += rew
        print("Episode reward", episode_rew)


if __name__ == '__main__':
    main()
