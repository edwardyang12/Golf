from gym.envs.registration import register

register(
    id='Golf-v0',
    entry_point='Golf.envs.golf_env:GolfEnv',
)
