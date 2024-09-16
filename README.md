# Protect your fivem scripts!

This is an open-source project that integrates a Python API, FiveM script, and a Discord bot to protect FiveM scripts from being leaked or used without a valid license key. The system requires a valid license key for each script to run, and without it, the script will not execute.

## Features
- **License Key Validation**: Ensures that each FiveM script has a unique license key.
- **Python API**: Manages license generation and validation.
- **FiveM Script**: Lua code for easy integration with your FiveM server.
- **Discord Bot Integration**: Monitor and manage licenses directly from Discord.
- **Open Source & Free**: Fully open-source under the MIT License.

## How It Works
1. **Python API**: Generates and validates license keys for each FiveM script.
2. **FiveM Script**: Lua code connects to the API to check for a valid license before running any script.
3. **Discord Bot**: Notifies and manages license statuses, offering an extra layer of monitoring.

## Requirements
- Python 3.x
- FiveM server
- Discord Bot Token
- `requests` Python library (for API communication)

## Setup Instructions

# Python API Installation
- Install Python 3.x
- Open Command Prompt - Python main.py

# Discord Bot Installation
- Change bot token - main.py - bot.run('Bot Token Here')

# FiveM Installation
- Change License key - Config.lua - Config.License = 'License Key Here'
