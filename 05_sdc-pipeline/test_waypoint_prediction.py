import gym
import numpy as np
import matplotlib.pyplot as plt
import pygame

from lane_detection import LaneDetection
from waypoint_prediction import waypoint_prediction, target_speed_prediction

# Initialize environment using gym.make()
env = gym.make('CarRacing-v2', render_mode='human')
env.reset()

# Define variables
total_reward = 0.0
steps = 0
restart = False

# Initialize modules of the pipeline
LD_module = LaneDetection()

# Initialize extra plot
fig = plt.figure()
plt.ion()
plt.show()

# Action variables
action = np.array([0.0, 0.0, 0.0])

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            env.close()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                action[0] = -1.0
            if event.key == pygame.K_RIGHT:
                action[0] = +1.0
            if event.key == pygame.K_UP:
                action[1] = +1.0
            if event.key == pygame.K_DOWN:
                action[2] = +0.8
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and action[0] == -1.0:
                action[0] = 0
            if event.key == pygame.K_RIGHT and action[0] == +1.0:
                action[0] = 0
            if event.key == pygame.K_UP:
                action[1] = 0
            if event.key == pygame.K_DOWN:
                action[2] = 0

    # Perform step
    observation, reward, done, truncated, info = env.step(action)
    env.render()

    # Lane detection
    lane1, lane2 = LD_module.lane_detection(observation)

    # Waypoint and target_speed prediction
    waypoints = waypoint_prediction(lane1, lane2)
    target_speed = target_speed_prediction(waypoints)

    # Update total reward
    total_reward += reward

    # Outputs during training
    if steps % 2 == 0 or done:
        print("\naction " + str(["{:+0.2f}".format(x) for x in action]))
        print("step {} total_reward {:+0.2f}".format(steps, total_reward))

        LD_module.plot_state_lane(observation, steps, fig, waypoints=waypoints)

    steps += 1

    # Check if stop
    if done or restart or steps >= 600:
        print("step {} total_reward {:+0.2f}".format(steps, total_reward))
        break

env.close()
