import tensorflow as tf
from tensorflow.keras import Sequential, layers

# for testing purposes
class Agent:
    def __init__(self, model):
        self.network = self.load_model(model)
        # idk what you want to initialize
        # not allowed to store position or any data about the agent here
        # can store something like your network or something

    # takes observations as input (position, height, wind)
    # outputs velocity, club number (see golf_env.py for more details)
    def step(self, observations):
        
        position = observations[0][0]
        height = observations[0][1]
        wind = observations[0][2]

        output = self.network.predict([observations])[0]
        return output

    def load_model(self, model):
        network = create_model()
        network.load_weights('./checkpoints/tester')
        return network

def create_model():
    model= Sequential()
    model.add(layers.Dense(128, input_shape=(3,)))
    model.add(layers.Dense(64))
    model.add(layers.Dense(2))
    model.compile(optimizer='sgd', loss='mse')
    return model



if __name__ == "__main__":
##    model = create_model()
##    model.save_weights('./checkpoints/tester')
      agent = Agent('./checkpoints/tester')
    
