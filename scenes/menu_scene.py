# scenes/menu_scene.py
import pygame
import config
from scenes.base_scene import BaseScene

class MenuScene(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font_large = pygame.font.SysFont("arial", 60)
        self.font_medium = pygame.font.SysFont("arial", 40)
        self.font_small = pygame.font.SysFont("arial", 24)
        
        # State: 'SELECT_KEYBOARD' or 'MAIN_MENU'
        self.state = 'SELECT_KEYBOARD'
        
        self.keyboard_options = [
            {'label': "61 Keys (Standard Portable)", 'keys': 61, 'range': (36, 96)},
            {'label': "88 Keys (Full Piano)", 'keys': 88, 'range': (21, 108)},
            {'label': "49 Keys (Compact)", 'keys': 49, 'range': (48, 84)}
        ]
        
        self.main_menu_options = [
            "1. Note Trainer",
            "2. Rhythm Trainer (Coming Soon)",
            "3. Chord Practice (Coming Soon)"
        ]

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                
                # --- LOGIC FOR KEYBOARD SELECTION ---
                if self.state == 'SELECT_KEYBOARD':
                    if event.key == pygame.K_1:
                        self.set_keyboard(0)
                    elif event.key == pygame.K_2:
                        self.set_keyboard(1)
                    elif event.key == pygame.K_3:
                        self.set_keyboard(2)

                # --- LOGIC FOR MAIN MENU ---
                elif self.state == 'MAIN_MENU':
                    if event.key == pygame.K_1:
                        print("Switching to Note Trainer...")
                        self.manager.switch_to('NOTE_TRAINER')
                    elif event.key == pygame.K_2:
                        self.manager.switch_to('RHYTHM_TRAINER')
                    elif event.key == pygame.K_ESCAPE:
                        # Allow going back to re-select keyboard
                        self.state = 'SELECT_KEYBOARD'

    def set_keyboard(self, index):
        """Saves the user choice to the global config."""
        selected = self.keyboard_options[index]
        config.USER_KEYBOARD_CONFIG = selected
        print(f"Config Saved: {config.USER_KEYBOARD_CONFIG}")
        self.state = 'MAIN_MENU'

    def process_midi(self, midi_messages):
        # Optional: Let them select with piano keys?
        pass

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(config.COLOR_BG)
        
        if self.state == 'SELECT_KEYBOARD':
            self.draw_keyboard_selection(screen)
        else:
            self.draw_main_menu(screen)

    def draw_keyboard_selection(self, screen):
        title = self.font_large.render("Welcome to OpenKeys", True, config.COLOR_ACCENT)
        subtitle = self.font_medium.render("Select your keyboard size:", True, config.COLOR_TEXT)
        
        # Center the title
        screen.blit(title, (config.SCREEN_WIDTH//2 - title.get_width()//2, 100))
        screen.blit(subtitle, (config.SCREEN_WIDTH//2 - subtitle.get_width()//2, 180))

        y = 300
        for i, option in enumerate(self.keyboard_options):
            text = f"[{i+1}] {option['label']}"
            render = self.font_medium.render(text, True, config.COLOR_TEXT)
            screen.blit(render, (config.SCREEN_WIDTH//2 - render.get_width()//2, y))
            y += 70

    def draw_main_menu(self, screen):
        # Show what is currently selected at the top right
        current_cfg = config.USER_KEYBOARD_CONFIG
        status_text = f"Config: {current_cfg['keys']} Keys"
        status_render = self.font_small.render(status_text, True, (100, 100, 100))
        screen.blit(status_render, (config.SCREEN_WIDTH - 200, 20))

        # Main Title
        title = self.font_large.render("Main Menu", True, config.COLOR_ACCENT)
        screen.blit(title, (50, 50))

        # Options
        y = 150
        for opt in self.main_menu_options:
            text = self.font_medium.render(opt, True, config.COLOR_TEXT)
            screen.blit(text, (50, y))
            y += 60
            
        help_text = self.font_small.render("Press number keys to select | ESC to go back", True, (150, 150, 150))
        screen.blit(help_text, (50, config.SCREEN_HEIGHT - 50))