import gym
from pyglet.window import key
import numpy as np
import pyglet

# Create the car racing environment without specifying render_mode
env = gym.make("CarRacing-v2")

# Define action mapping for steering, acceleration, and braking
action = np.array([0.0, 0.0, 0.0], dtype=np.float32)

def key_press(symbol, modifiers):
    global action
    if symbol == key.LEFT:
        action[0] = -1.0   # Steer left
    elif symbol == key.RIGHT:
        action[0] = +1.0   # Steer right
    elif symbol == key.UP:
        action[1] = +1.0   # Accelerate (gas)
    elif symbol == key.DOWN:
        action[2] = +0.8   # Brake

def key_release(symbol, modifiers):
    global action
    if symbol == key.LEFT and action[0] == -1.0:
        action[0] = 0.0
    elif symbol == key.RIGHT and action[0] == +1.0:
        action[0] = 0.0
    elif symbol == key.UP:
        action[1] = 0.0
    elif symbol == key.DOWN:
        action[2] = 0.0

# Initialize the environment and get the initial frame
observation, info = env.reset()
frame = observation

# Determine frame dimensions
height, width, _ = frame.shape

# Set the window size (maintain aspect ratio)
window_width = 600
window_height = int(window_width * (height / width))  # Keep the aspect ratio

# Create a Pyglet window to display the game
window = pyglet.window.Window(width=window_width, height=window_height, caption="Manual Car Driving")
window.push_handlers(on_key_press=key_press, on_key_release=key_release)

@window.event
def on_draw():
    window.clear()
    # Convert the frame to a format suitable for Pyglet
    image_data = pyglet.image.ImageData(
        width, height, 'RGB', frame.tobytes(), pitch=-width * 3
    )
    # Scale the image to fit the window
    image_data.blit(0, 0, width=window.width, height=window.height)

def update(dt):
    global frame
    # Apply the action and get the new observation (frame)
    observation, reward, done, truncated, info = env.step(action)
    frame = observation
    if done or truncated:
        observation, info = env.reset()
        frame = observation

# Schedule the update loop to run at 60 FPS
pyglet.clock.schedule_interval(update, 1.0 / 60.0)

# Run the Pyglet event loop
pyglet.app.run()

env.close()
