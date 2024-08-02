### Features
1. Panel to add/subtract time/points
2. Convert mathematically based on type of support given
3. obs/Timer.txt and obs/Points.txt to hook into OBS; files generated on first program run
4. a 'ledger' that tracks most recent 5 actions
5. crash proof; since the clock is based on math done on system time since less action in relation to current system time-- program can be turned off and on with no issue or lost details

# Project Setup Guide

This guide will walk you through setting up and running the project on a Windows environment. It covers reinstalling Python, configuring system environment variables, installing necessary packages, running the application, and setting up OBS (Open Broadcaster Software) for displaying the timer.

## Step 1: Reinstall Python and Set Path in System Settings

### Installing Python

1. Download the Python installer from the [official Python website](https://www.python.org/downloads/).
2. Run the installer. Ensure to check the box **"Add Python 3.x to PATH"** at the bottom of the first installation window.
3. Follow the installation prompts to complete the installation.

### Verifying Python Installation

Open Command Prompt in ADMIN MODE and paste in:
```bash
python --version
```
This should display the Python version if it was installed correctly and added to PATH.

## Step 2: Install Project Requirements

1. Navigate to your project directory in Command Prompt:
```bash
cd path\to\your\project
```
2. Install the required packages using pip:
```bash
pip install -r requirements.txt
```

## Step 3: Run the Application

From your project directory in Command Prompt, run:
```bash
python main.py
```
This command starts the server on your local machine.

## Step 4: Open the Website

Open a web browser and go to:
```bash
http://127.0.0.1:5050/
```
This URL will take you to the hosted application on your local server; this is where you input cheese, youtube, memberships, streamlabs, and more.

## Step 5: Setup OBS for Displaying the Timer
This is the output of your instance. 
### Adding Timer to OBS

1. **Open OBS**.
2. In the **Sources** panel, click on the **+** (add) button.
3. Select **Text (GDI+)** and name your source (e.g., "Timer").
4. Check the box **"Read from file"** and then browse to select the `obs/timer.txt` file in your project directory.
5. Customize the font and style as desired.

### Positioning and Styling

- Drag the text source to position it within your OBS scene.
- Use the properties menu for the text source to adjust font size, color, and other styling options to fit your streaming setup.


