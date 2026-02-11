import pygame
import config

# Standard Piano Dimensions
WHITE_KEY_WIDTH = 0  # Will be calculated dynamically
WHITE_KEY_HEIGHT = 200
BLACK_KEY_WIDTH_RATIO = 0.6
BLACK_KEY_HEIGHT_RATIO = 0.65

# Colors
COLOR_WHITE_KEY = (240, 240, 240)
COLOR_BLACK_KEY = (20, 20, 20)
COLOR_ACTIVE = (100, 200, 255)  # Blue for pressed keys
COLOR_TARGET = (50, 200, 50)    # Green for correct keys
COLOR_WRONG = (200, 50, 50)     # Red for wrong keys

class VirtualPiano:
    def __init__(self, start_note, end_note, x, y, width, height):
        self.start_note = start_note  # e.g., 36 (C2)
        self.end_note = end_note      # e.g., 96 (C7)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Pre-calculate key positions
        self.white_keys = []
        self.black_keys = []
        self._generate_keys()

    def _generate_keys(self):
        """Calculates the rectangle for every key based on the range."""
        
        # 1. Count how many white keys we need
        num_white_keys = 0
        for midi_num in range(self.start_note, self.end_note + 1):
            if not self._is_black_key(midi_num):
                num_white_keys += 1
        
        # 2. Calculate dynamic width
        key_w = self.width / num_white_keys
        black_key_w = key_w * BLACK_KEY_WIDTH_RATIO
        black_key_h = self.height * BLACK_KEY_HEIGHT_RATIO

        # 3. Generate Rects
        current_x = self.x
        
        # We need two passes: White keys first (background), Black keys second (foreground)
        # But we iterate note-by-note to track positions
        
        for midi_num in range(self.start_note, self.end_note + 1):
            is_black = self._is_black_key(midi_num)
            
            if not is_black:
                # It's a white key
                rect = pygame.Rect(current_x, self.y, key_w - 1, self.height) # -1 for gap
                self.white_keys.append({'note': midi_num, 'rect': rect})
                current_x += key_w
            else:
                # It's a black key - Draw it shifted back by half a width
                # Note: Black keys don't advance current_x!
                rect = pygame.Rect(current_x - (black_key_w / 2), self.y, black_key_w, black_key_h)
                self.black_keys.append({'note': midi_num, 'rect': rect})

    def _is_black_key(self, midi_num):
        """Returns True if the midi number corresponds to a sharp/flat."""
        # Pattern of black keys in an octave (0=C, 1=C#, etc.)
        # 0  1  2  3  4  5  6  7  8  9 10 11
        # W  B  W  B  W  W  B  W  B  W  B  W
        index = midi_num % 12
        return index in [1, 3, 6, 8, 10]

    def draw(self, screen, active_notes=None, target_note=None):
        """
        Draws the piano.
        active_notes: list or set of MIDI numbers currently pressed.
        target_note: a specific note to highlight (optional).
        """
        if active_notes is None:
            active_notes = set()

        # 1. Draw White Keys
        for key in self.white_keys:
            color = COLOR_WHITE_KEY
            if key['note'] in active_notes:
                # Check if it's the target or just a press
                if key['note'] == target_note:
                    color = COLOR_TARGET
                elif target_note is not None:
                     # If there is a target but we pressed this, it's wrong
                    color = COLOR_WRONG
                else:
                    color = COLOR_ACTIVE
            
            pygame.draw.rect(screen, color, key['rect'])
            # Draw highlight for target if user ISN'T pressing it
            if target_note == key['note'] and key['note'] not in active_notes:
                pygame.draw.rect(screen, COLOR_TARGET, key['rect'], 3) # Outline only

        # 2. Draw Black Keys
        for key in self.black_keys:
            color = COLOR_BLACK_KEY
            if key['note'] in active_notes:
                if key['note'] == target_note:
                    color = COLOR_TARGET
                elif target_note is not None:
                    color = COLOR_WRONG
                else:
                    color = COLOR_ACTIVE

            pygame.draw.rect(screen, color, key['rect'])
             # Draw highlight for target if user ISN'T pressing it
            if target_note == key['note'] and key['note'] not in active_notes:
                pygame.draw.rect(screen, COLOR_TARGET, key['rect'], 2) # Outline only