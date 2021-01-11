# test agent
import random
import gym
import Golf

env = gym.make('Golf-v0')

total_reward = 0
for i in range(5):
    episode_reward = 0
    env.reset()
    for t in range(10):

        # agent should determine action based on observation
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        print("Observations: {} ".format(observation))
        print("Reward: {} ".format(reward))
        print("Action: {} ".format(action))
        
        episode_reward += reward
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
    total_reward += episode_reward

print("Simulation finished with reward: {} ".format(total_reward/5))

    
