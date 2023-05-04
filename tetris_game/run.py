
from tetris import Tetris
import random
        

# # Run dqn with Tetris
# def dqn():
    


#     scores = []

#         # Game
#         while not done and (not max_steps or steps < max_steps):
#             next_states = env.get_next_states()
#             best_state = agent.best_state(next_states.values())
            
#             best_action = None
#             for action, state in next_states.items():
#                 if state == best_state:
#                     best_action = action
#                     break

#             reward, done = env.play(best_action[0], best_action[1], render=render,
#                                     render_delay=render_delay)
            
#             agent.add_to_memory(current_state, next_states[best_action], reward, done)
#             current_state = next_states[best_action]
#             steps += 1

if __name__ == "__main__":

    env = Tetris()
    episodes = 2000
    max_steps = None
    epsilon_stop_episode = 1500
    mem_size = 20000
    discount = 0.95
    batch_size = 512
    epochs = 1
    render_every = 50
    log_every = 50
    replay_start_size = 2000
    train_every = 1
    n_neurons = [32, 32]
    render_delay = None
    activations = ['relu', 'relu', 'linear']
    steps = 1

    while not done and (not max_steps or steps < max_steps):
            next_states = env.get_next_states()
            

            reward, done = env.play(0,0, render=True,
                                    render_delay=render_delay)
            steps += 1