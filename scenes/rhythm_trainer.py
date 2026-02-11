import pygame
import random
import config
from scenes.base_scene import BaseScene
from core.graphics import VirtualPiano

class FallingNote:
    def __init__(self, midi_num, lane_x, lane_width, spawn_y, target_y, speed):
        self.midi_num = midi_num
        self.rect = pygame.Rect(lane_x, spawn_y, lane_width, 40) # 40px height note
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.target_y = target_y
        self.speed = speed # Pixels per frame
        self.active = True
        self.hit = False

    def update(self):
        self.rect.y += self.speed
        
    def draw(self, screen):
        # Draw the main note body
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw a border
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

class RhythmTrainerScene(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.SysFont("arial", 30)
        
        # 1. Setup Piano (Same as Note Trainer)
        if config.USER_KEYBOARD_CONFIG:
            start, end = config.USER_KEYBOARD_CONFIG['range']
        else:
            start, end = 36, 96 

        piano_height = 150
        self.piano_y = config.SCREEN_HEIGHT - piano_height - 20
        self.piano = VirtualPiano(
            start_note=start, 
            end_note=end, 
            x=50, y=self.piano_y, 
            width=config.SCREEN_WIDTH - 100, 
            height=piano_height
        )

        # 2. Game Settings
        self.scroll_speed = 3  # Pixels per frame
        self.spawn_timer = 0
        self.spawn_rate = 120  # Spawn a note every 120 frames (approx 2 seconds)
        
        self.notes = [] # List of FallingNote objects
        self.score = 0
        self.misses = 0
        self.held_keys = set()

    def _spawn_note(self):
        # 1. Pick a random note in range
        note_num = random.randint(self.piano.start_note, self.piano.end_note)
        
        # 2. Find the X position of that key on the piano
        # We need to ask the piano where this key is. 
        # Since VirtualPiano pre-calculates rects, we can look it up!
        
        target_key_rect = None
        # Check white keys
        for k in self.piano.white_keys:
            if k['note'] == note_num:
                target_key_rect = k['rect']
                break
        # Check black keys
        if not target_key_rect:
            for k in self.piano.black_keys:
                if k['note'] == note_num:
                    target_key_rect = k['rect']
                    break
        
        if target_key_rect:
            new_note = FallingNote(
                midi_num=note_num,
                lane_x=target_key_rect.x,
                lane_width=target_key_rect.width,
                spawn_y=-50, # Start just above screen
                target_y=self.piano_y,
                speed=self.scroll_speed
            )
            self.notes.append(new_note)

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.switch_to('MENU')

    def process_midi(self, midi_messages):
        for msg in midi_messages:
            if msg.type == 'note_on' and msg.velocity > 0:
                self.held_keys.add(msg.note)
                self.check_hit(msg.note)
            
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in self.held_keys:
                    self.held_keys.remove(msg.note)

    def check_hit(self, played_note):
        """Logic to see if the user hit a note at the right time."""
        hit_zone = 50 # Pixels tolerance (roughly the height of a falling note)
        
        for note in self.notes:
            if note.active and not note.hit and note.midi_num == played_note:
                # Check distance to the "Hit Line" (piano_y)
                distance = abs(note.rect.y - self.piano_y)
                
                if distance < hit_zone:
                    note.hit = True
                    note.active = False # Remove it
                    self.score += 10
                    print("Hit!")
                    return # Only hit the lowest note per key press

    def update(self):
        # 1. Spawner
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_rate:
            self._spawn_note()
            self.spawn_timer = 0

        # 2. Move Notes
        for note in self.notes:
            note.update()
            
            # Check Miss (Passed the piano)
            if note.active and note.rect.y > config.SCREEN_HEIGHT:
                note.active = False
                self.misses += 1
                print("Miss!")

        # 3. Cleanup inactive notes
        self.notes = [n for n in self.notes if n.active]

    def draw(self, screen):
        screen.fill(config.COLOR_BG)

        # Draw "Lane Lines" (Optional visuals to make it look cool)
        # pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, height))

        # Draw Notes
        for note in self.notes:
            note.draw(screen)

        # Draw Piano (Foreground)
        # We pass active notes so keys light up when you play
        self.piano.draw(screen, active_notes=self.held_keys)

        # Draw HUD
        score_text = self.font.render(f"Score: {self.score}", True, config.COLOR_SUCCESS)
        miss_text = self.font.render(f"Misses: {self.misses}", True, config.COLOR_FAIL)
        screen.blit(score_text, (20, 20))
        screen.blit(miss_text, (20, 60))