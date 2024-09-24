import numpy as np
import gym
import pygame
import logging
import matplotlib.pyplot as plt
from lane_detection import LaneDetection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def initialize_environment(env_name='CarRacing-v2', render_mode='human'):
    """Initialize the Gym environment and return it."""
    env = gym.make(env_name, render_mode=render_mode)
    return env

def initialize_pygame(fps=60):
    """Initialize Pygame and return a clock object."""
    pygame.init()
    return pygame.time.Clock(), fps

def process_input(key_bindings, steering_sensitivity=1.0, action_intensity=1.0):
    """Process Pygame input and return an action array with customized key bindings."""
    action = [0.0, 0.0, 0.0]  # [steer, gas, brake]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return action, True  # Quit signal received, stop driving

    keys = pygame.key.get_pressed()
    if keys[key_bindings['quit']]:
        return action, True  # Stop on quit key (ESC)
    if keys[key_bindings['left']]:
        action[0] = -steering_sensitivity  # Steer left
    if keys[key_bindings['right']]:
        action[0] = +steering_sensitivity  # Steer right
    if keys[key_bindings['gas']]:
        action[1] = +action_intensity  # Gas
    if keys[key_bindings['brake']]:
        action[2] = +action_intensity  # Brake
    
    return action, False

def handle_step(env, action):
    """Perform a step in the environment and return updated information."""
    observation, reward, terminated, truncated, info = env.step(action)
    return observation, reward, terminated, truncated

def game_loop(env, clock, fps, key_bindings, steering_sensitivity, action_intensity):
    """Main game loop where the action and environment are updated."""
    total_reward = 0.0
    observation, _ = env.reset()
    done = False

    # Initialize lane detection module
    LD_module = LaneDetection()

    # Initialize extra plot
    fig = plt.figure()
    plt.ion()
    plt.show()

    steps = 0
    while not done:
        action, quit_signal = process_input(key_bindings, steering_sensitivity, action_intensity)
        if quit_signal:
            done = True
            break

        observation, reward, terminated, truncated = handle_step(env, action)
        total_reward += reward
        env.render()
        
        # Perform lane detection
        splines = LD_module.lane_detection(observation)

        # Plot lane detection results
        if steps % 2 == 0 or terminated:
            logging.info(f"Action: {['{:+0.2f}'.format(x) for x in action]}, Step: {steps}, Total Reward: {total_reward:.2f}")
            LD_module.plot_state_lane(observation, steps, fig)

        clock.tick(fps)
        steps += 1

        if terminated or truncated:
            logging.info(f"Episode ended. Total reward: {total_reward}")
            observation, _ = env.reset()

    return total_reward

def close_environment(env):
    """Close the environment and quit Pygame."""
    env.close()
    pygame.quit()

def drive(env_name='CarRacing-v2', render_mode='human', fps=60, steering_sensitivity=1.0, action_intensity=1.0, key_bindings=None):
    """Main function to run the car driving simulation with customizable parameters."""
    
    # Default key bindings if none provided
    if key_bindings is None:
        key_bindings = {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'gas': pygame.K_UP,
            'brake': pygame.K_DOWN,
            'quit': pygame.K_ESCAPE
        }
    
    logging.info("Initializing environment...")
    env = initialize_environment(env_name, render_mode)
    
    logging.info(f"Initialized environment: {env_name}")
    clock, fps = initialize_pygame(fps)

    logging.info("Starting game loop...")
    total_reward = game_loop(env, clock, fps, key_bindings, steering_sensitivity, action_intensity)

    logging.info(f"Total reward for this session: {total_reward}")
    logging.info("Closing environment...")
    close_environment(env)

if __name__ == "__main__":
    # Define custom parameters
    custom_key_bindings = {
        'left': pygame.K_a,    # Steer left with 'A'
        'right': pygame.K_d,   # Steer right with 'D'
        'gas': pygame.K_w,     # Gas with 'W'
        'brake': pygame.K_s,   # Brake with 'S'
        'quit': pygame.K_q     # Quit with 'Q'
    }

    drive(
        env_name='CarRacing-v2',
        render_mode='human',
        fps=60,
        steering_sensitivity=1.0,  # Customize steering sensitivity
        action_intensity=1.0,      # Customize gas/brake intensity
        key_bindings=custom_key_bindings  # Use custom key bindings
    )
