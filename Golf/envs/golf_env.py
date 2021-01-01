import gym
from gym import spaces
import math
import random
import numpy as np

# 2D golf where objective is for player to put the ball into the hole
# farthest can launch ball is shorter than distance to hole
# Start and end height constant
# Wind changes per hit
# Different clubs with different amounts of "power" and different preset angles
# intuition is that with these different angles, wind will affect them by different amounts
# Outputs: distance to hole and to each trap state
# Input: which club to use and how far to launch

# next iteration will add these:
# Must avoid traps held constant per map
# map of where ball is (including traps),

'''
driver = 10 -> 0
5- iron = 27 -> 1
9- iron = 42 -> 2
lofting wedge = 60 -> 3
'''

time = 0.01
gravity = -9.81

class GolfEnv(gym.Env):

    def __init__(self):
        super(GolfEnv,self).__init__()

        ''' for golf course initialization stuff '''
        self.max_dist = 2000 # meters of longest track
        self.clubs = {0:10,1:27,2:42,3:60}
        self.min_dist = 400
        self.reached = 5 # within 5 meters means u got it
        self.obstacles = 0 # traps
        self.steps = 10 # only get 10 golf swings


        # first iteration just power no golf clubs
        self.action_space = spaces.Box(low=np.array([0]),high=np.array([50]))
        high = np.array([1]*(2*(self.obstacles+1)))
        high = np.append(high,5)
        low = np.array([0]*(2*(self.obstacles+1)))
        low = np.append(low,-5)
        self.observation_space = spaces.Box(
            low = low,
            high = high,
            dtype=np.float32
        )

        self.reset()

    def generate_track(self):
        self.dist = random.randint(self.min_dist,self.max_dist)
        self.max_obstacle_size = self.dist/4
        size_array = [random.randint(0,int(self.max_obstacle_size/2)) for _ in range(self.obstacles)]
        start = 0
        for size in size_array:
            end = random.randint(start,start+size)
            self.obstacles_array.append([start,end])
            start = 2*end
        self.obstacles_array.append([start,self.dist])

    def step(self,action):

        velocity = action
        # club, velocity = action
        # angle = self.clubs[club]
        angle = self.clubs[1]
        distance = self.calcLocation(velocity, angle)

        self.curr += distance
        self.path.append(self.curr)

        trapped = True
        for tuple in self.obstacles_array:
            if self.curr>tuple[0] and self.curr<tuple[1]:
                trapped = False
                break

        # exceeded bounds
        if self.curr<0:
            print("backwards")
            output = np.array([1]*(2*(self.obstacles+1)))
            output = np.append(output,self.wind)
            return output, -1, True, {}
        elif self.curr>self.dist:
            print("over")
            output = np.array([1]*(2*(self.obstacles+1)))
            output = np.append(output,self.wind)
            return output, -1, True, {}

        distance = abs(self.dist-self.curr)
        if distance < self.reached:
            return self._get_obs(), 1, True, {}
        else:
            self.runtime +=1

            # trapped or exceeded max steps
            if trapped or self.runtime>=self.steps:
                return self._get_obs(), -1, True, {}

            obs = self._get_obs()
            self.wind = random.randint(-5, 5)
            return obs, 1-distance/self.dist, False, {}

    def _get_obs(self):
        temp = np.array(self.obstacles_array)-self.curr
        temp = np.abs(temp)/self.dist
        temp = np.append(temp,self.wind)
        return temp

    def calcLocation(self, velocity, angle):

        horizontal_vel = velocity * math.cos(angle * math.pi / 180)
        vertical_vel = velocity * math.sin(angle * math.pi / 180)
        horizontal_dist = 0
        vertical_dist = 0

        while((vertical_dist> 0) or (vertical_vel>0)):
            horizontal_dist = horizontal_vel * time + horizontal_dist
            vertical_dist = vertical_vel * time + vertical_dist
            vertical_vel = vertical_vel + gravity * time
            horizontal_vel = horizontal_vel + self.wind

        return horizontal_dist

    def reset(self):
        self.wind = random.randint(-5, 5)
        self.runtime = 0
        self.dist = 0
        self.curr = 0
        self.obstacles_array = []
        self.generate_track()
        return self._get_obs()

    def render(self, mode='human', close=False):
        if not close:
            print("target: " + str(self.dist))
            print("path: " + str(self.path))

if __name__ == "__main__":
    env = GolfEnv()
    print(env._get_obs())
    for i in range(20):
        obs,reward, bool, _ = env.step(25)
        if(bool and reward ==-1):
            print("backwards or exceeded")
            print(obs, reward)
            break
        elif(bool and reward==1):
            print("success")
            print(obs,reward)
            break
        else:
            print(obs,reward)
