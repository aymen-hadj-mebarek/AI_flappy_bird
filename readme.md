# Flappy Bird AI using NEAT and Pygame

This project is an implementation of a Flappy Bird game with an AI agent trained using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The AI learns to play the game by evolving over generations, improving its performance by adjusting the neural network weights.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Credits](#credits)

## Introduction

This project uses the NEAT algorithm to train a neural network that can play the Flappy Bird game. The game and training are implemented using Python's Pygame library. The AI starts with random movements and evolves through generations to optimize its gameplay.

## Features

- **Flappy Bird Game**: Classic Flappy Bird gameplay implemented in Pygame.
- **AI Training**: AI is trained using the NEAT algorithm.
- **Neural Network**: The AI uses a neural network to decide whether to jump or not.
- **Fitness Evaluation**: The AI's performance is evaluated based on its ability to avoid obstacles.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/flappy-bird-neat.git
   cd flappy-bird-neat
   ```
2. **Install Dependencies:**

You need Python 3.x installed. Install the required Python packages using pip:

    
   ```bash
    pip install -r requirements.txt     #(Ensure you have the following dependencies: Pygame and NEAT-Python.)
   ```

3. **Add Game Assets:**

Ensure that the image files for the bird, pipes, base, and background are located in the imgs/ directory.

## Usage
To run the game and start the AI training, execute the following command:
    
   ```bash
    python flappy_bird_neat.py
   ```

## Project Structure

   ```bash
flappy-bird-neat/
│
├── imgs/                       # Directory containing game assets (images)
│   ├── bird1.png
│   ├── bird2.png
│   ├── bird3.png
│   ├── pipe.png
│   ├── base.png
│   └── bg.png
│
├── flappy_bird_neat.py         # Main game and AI training script
├── NEAT_config.txt             # NEAT configuration file
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
   ```

## Configuration
The NEAT algorithm's parameters are configured in the NEAT_config.txt file. You can adjust various settings like population size, mutation rates, and more to tweak the AI's training process.

## Dependencies
- Python 3.x
- Pygame
- NEAT-Python
\\ You can install all dependencies via the requirements.txt file.

## Credits
This project was developed as a demonstration of the NEAT algorithm combined with the classic Flappy Bird game.