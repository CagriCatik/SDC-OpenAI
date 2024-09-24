# SDC-OpenAI

This project includes a variety of approaches, such as **Imitation Learning** and **Reinforcement Learning**, to train self-driving models. Additionally, it features control design exercises and a full pipeline for developing autonomous car systems.

## Project Overview

This project provides multiple learning approaches to teach self-driving cars in simulated environments. Whether you're interested in **manually controlling** a car in **OpenAI Gym's CarRacing-v2** or exploring **machine learning techniques** like imitation and reinforcement learning, this repository has you covered.

### Core Learning Methods

- **Imitation Learning**: Train models by mimicking human driving behavior.
- **Reinforcement Learning**: Learn to drive through trial and error by rewarding successful actions.
- **Control Design**: Fine-tune control algorithms for autonomous vehicle dynamics.

---

## Features

- **Manual Driving Mode**: Experience real-time car control through keyboard inputs in OpenAI Gym's CarRacing-v2 environment.
- **Comprehensive Learning Modules**: Includes exercises and pipelines for learning via imitation, reinforcement learning, and control systems.
- **Automated Setup**: The project includes an `install_dependencies.sh` script to handle setup and dependencies.
- **Cross-Platform Compatibility**: Works seamlessly on Linux, macOS, and Windows.

---

## Project Structure

This repository is organized into distinct sections to facilitate learning and experimentation:

1. **Introduction**: Introduction to self-driving cars and the OpenAI Gym environment.
2. **Imitation Learning**: Modules and scripts to implement imitation learning.
3. **Reinforcement Learning**: Experiments with reinforcement learning to develop driving policies.
4. **Control Design Exercises**: Exercises to practice and improve control systems for autonomous cars.
5. **SDC Pipeline**: End-to-end pipeline for building and evaluating self-driving car models.

---

## Installation Guide

Before getting started, ensure your system meets the following prerequisites:

### Prerequisites

- **Python**: Version 3.7 or higher.
- **Operating System**: Ubuntu/Debian-based Linux distributions are recommended. macOS and Windows support are available but may require additional setup.
- **System Dependencies**:
  - `python3-dev`
  - `python3-pip`
  - `python3-venv`
  - `libgl1-mesa-glx`
  - `libglu1-mesa`
  - `swig`
  - `xvfb` (Optional: For virtual framebuffer rendering)

### Steps to Install

#### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/CagriCatik/SDC-OpenAI
cd SDC-OpenAI
```

#### 2. Run the Installation Script

The provided `install_dependencies.sh` script automates the installation process.

Make the script executable:

```bash
chmod +x install_dependencies.sh
```

Now, run the script:

```bash
./install_dependencies.sh
```

This script will:

- Update system packages
- Install necessary system dependencies
- Set up a Python virtual environment
- Install all required Python packages

#### 3. Activate the Virtual Environment

Once the installation is complete, activate the virtual environment:

```bash
source venv/bin/activate
```

---

## How to Use

Once the environment is set up, you can manually control a car in the CarRacing-v2 environment. Run the following command to start the simulation:

```bash
python manual_car_driving.py
```

---

## Controls

Here are the keyboard controls for manually driving the car:

- **Left Arrow (←)**: Steer Left
- **Right Arrow (→)**: Steer Right
- **Up Arrow (↑)**: Accelerate
- **Down Arrow (↓)**: Brake
