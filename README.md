# APCSP-Create-Project
My 2025 AP Computer Science Principles Create Project

# Barbell Weight Visualizer

A terminal-based Python program to help weightlifters calculate, visualize, and manage the weights on their barbell. Designed for simplicity and accuracy, with an ASCII art visualization of the bar with colored plates.

<img width="50%" alt="Screenshot of ASCII art barbell" src="https://github.com/user-attachments/assets/66647950-600d-43f8-bba1-849d06daf9b4" />

## Features

- Manually add/remove individual plate sizes  
- Solve for a target weight respecting plates already on the bar
- Toggle between 45lb and 35lb bars
- Clear current setup  
- View real-time ASCII art of your bar with colored plates  
- Converts total weight to kilograms in real time 

## Usage
Run the program and use the following commands:

```bash
  add <weight>     Add a weight of <weight> lb to your bar. Example: add 35
  remove <weight>  Remove a weight of <weight> lb to your bar. Will have no effect when weight is not on your bar. Example: remove 35
  solve <weight>   Set your bar to <weight> lb using calculated plates. Keeps preexisting plates. Example: solve 227
  bar              Swap the bar between 45lb and 35lb. Example: bar
  clear            Remove all weights. Example: clear
  exit             Exit program. Example: exit
