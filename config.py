# config.py
import pygame

# Screen Settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
COLOR_BG = (30, 30, 30)
COLOR_TEXT = (255, 255, 255)
COLOR_ACCENT = (100, 200, 255)
COLOR_SUCCESS = (50, 200, 50)
COLOR_FAIL = (200, 50, 50)

# Global State
# This will be updated by the Menu Scene
# Format: {'keys': 61, 'range': (36, 96)}
USER_KEYBOARD_CONFIG = None 

# Initial MIDI setup
MIDI_DEVICE_NAME = None