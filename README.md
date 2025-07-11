# Coin Collector Game

A simple 2D game built with Python and Pygame where you collect coins while avoiding obstacles.

## Game Features

- Control a player character using arrow keys
- Collect coins to increase your score
- Avoid obstacles
- Score tracking
- Smooth movement and collision detection

## Prerequisites

- Python 3.6 or higher
- Virtual environment (instructions below)

## Setup Instructions

1. Clone or download this repository to your local machine

2. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

1. Start the game:
```bash
python game.py
```

2. Game Controls:
   - LEFT ARROW: Move player left
   - RIGHT ARROW: Move player right
   - Close window to quit game

3. Game Rules:
   - Collect yellow coins to increase your score
   - Avoid red obstacles
   - Game ends if you hit an obstacle

## Game Elements

- White Square: Player character
- Yellow Circles: Coins to collect
- Red Squares: Obstacles to avoid
- Score Counter: Top-left corner of the screen