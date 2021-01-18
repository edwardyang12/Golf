class Agent:
    def __init__(self):
        self.network = None
        # idk what you want to initialize
        # not allowed to store position or any data about the agent here
        # can store something like your network or something

    # takes observations as input (position, height, wind)
    # outputs velocity, club number (see golf_env.py for more details)
    def step(self, observations):
        position = observations[0]
        height = observations[1]
        wind = observations[2]

        return [0,0]
