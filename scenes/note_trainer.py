import pygame
import random
import config
from scenes.base_scene import BaseScene
from core.graphics import VirtualPiano

class NoteTrainerScene(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font_large = pygame.font.SysFont("arial", 80)
        self.font_small = pygame.font.SysFont("arial", 30)

        # 1. Setup Piano Visualizer
        # We get the user's config (e.g., 61 keys)
        if config.USER_KEYBOARD_CONFIG:
            start, end = config.USER_KEYBOARD_CONFIG['range']
        else:
            # Fallback if config is missing (debugging)
            start, end = 36, 96 

        # Create the piano at the bottom of the screen
        piano_height = 200
        self.piano = VirtualPiano(
            start_note=start,
            end_note=end,
            x=50, 
            y=config.SCREEN_HEIGHT - piano_height - 50,
            width=config.SCREEN_WIDTH - 100,
            height=piano_height
        )

        # 2. Game State
        self.score = 0
        self.target_note = self._get_new_note()
        self.feedback_text = "Find the note!"
        self.feedback_color = config.COLOR_TEXT
        
        # Track currently held keys for visual feedback
        self.held_keys = set()

    def _get_new_note(self):
        """Pick a random note within the user's range."""
        start, end = self.piano.start_note, self.piano.end_note
        return random.randint(start, end)

    def _midi_to_name(self, midi_num):
        names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        idx = midi_num % 12
        octave = (midi_num // 12) - 1
        return f"{names[idx]}{octave}"

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Go back to menu
                    self.manager.switch_to('MENU')

    def process_midi(self, midi_messages):
        for msg in midi_messages:
            if msg.type == 'note_on' and msg.velocity > 0:
                self.held_keys.add(msg.note)
                
                # Check Game Logic
                if msg.note == self.target_note:
                    self.score += 1
                    self.feedback_text = "Correct!"
                    self.feedback_color = config.COLOR_SUCCESS
                    self.target_note = self._get_new_note()
                else:
                    self.feedback_text = f"Wrong! That was {self._midi_to_name(msg.note)}"
                    self.feedback_color = config.COLOR_FAIL
            
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in self.held_keys:
                    self.held_keys.remove(msg.note)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(config.COLOR_BG)

        # 1. Draw UI Text
        target_name = self._midi_to_name(self.target_note)
        
        # Draw "Question"
        text_surf = self.font_large.render(f"Find: {target_name}", True, config.COLOR_ACCENT)
        text_rect = text_surf.get_rect(center=(config.SCREEN_WIDTH//2, 150))
        screen.blit(text_surf, text_rect)

        # Draw "Feedback"
        feedback_surf = self.font_small.render(self.feedback_text, True, self.feedback_color)
        feedback_rect = feedback_surf.get_rect(center=(config.SCREEN_WIDTH//2, 220))
        screen.blit(feedback_surf, feedback_rect)
        
        # Draw Score
        score_surf = self.font_small.render(f"Score: {self.score}", True, config.COLOR_TEXT)
        screen.blit(score_surf, (20, 20))

        # 2. Draw the Virtual Piano
        # We pass in held_keys so it lights up what we play
        # We pass in target_note so it hints what we SHOULD play
        self.piano.draw(screen, active_notes=self.held_keys, target_note=self.target_note)