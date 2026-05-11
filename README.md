# Shiny ball
Using Phong model

# Installation
There are 2 ways of doing it:
1. If you have installed python and want to use pip:
  - Create virtual environment: `python -m venv .venv`
  - Activate environment: `source .venv/bin/activate`
  - Install dependencies: `pip install -r requirements.txt`

2. If you wish to use uv:
  - Install with: `uv sync`

When the environment is prepared:

Run the program: `sudo ./.venv/bin/python3 main.py`

OR

Use starting script: one time `sudo chmod +x ./run.sh` then `sudo ./run.sh`

Program requires sudo because of reading keyboard signals access.

# Controls
You can move light source position:
  - w, s, a, d - up / down / left / right relatively to the camera
  - q, e - inward / outward
  - esc - closing program (manual closing is NOT a solution)