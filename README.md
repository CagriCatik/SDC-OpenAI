# Self Driving Cars in OpenAI Gym's

This project allows you to manually control a car in OpenAI Gym's `CarRacing-v2` environment using your keyboard. Experience real-time car racing by steering, accelerating, and braking as you navigate through the race track.

## Features

- **Interactive Controls**: Steer the car using keyboard inputs.
- **Real-Time Rendering**: Visualize the environment using Pyglet.
- **Automated Setup**: A bash script is provided for easy installation of all dependencies.
- **Cross-Platform**: Compatible with Windows, macOS, and Linux.

## Prerequisites

- **Python 3.7 or higher**
- **Operating System**: Linux (Ubuntu/Debian-based systems are recommended)
- **System Dependencies**:
  - `python3-dev`
  - `python3-pip`
  - `python3-venv`
  - `libgl1-mesa-glx`
  - `libglu1-mesa`
  - `swig`
  - `xvfb` (Optional: For virtual framebuffer)

## Installation

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/CagriCatik/SDC-OpenAI
cd SDC-OpenAI
```

### 2. Run the Installation Script

An `install_dependencies.sh` bash script is provided to automate the installation process.

#### 2.1. Make the Script Executable

```bash
chmod +x install_dependencies.sh
```

#### 2.2. Run the Script

```bash
./install_dependencies.sh
```

This script will:

- Update and upgrade system packages
- Install necessary system dependencies
- Create and activate a virtual environment
- Install all required Python packages

### 3. Activate the Virtual Environment

After the script completes, activate the virtual environment:

```bash
source venv/bin/activate
```

### 4. Run the Manual Car Driving Script

```bash
python manual_car_driving.py
```

## Controls

- **Left Arrow (`←`)**: Steer Left
- **Right Arrow (`→`)**: Steer Right
- **Up Arrow (`↑`)**: Accelerate
- **Down Arrow (`↓`)**: Brake