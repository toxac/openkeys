import pygame
import mido
import sys
import random

# --- Constants ---
WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (100, 200, 255)  # Light Blue
SUCCESS_COLOR = (50, 200, 50)   # Green
FAIL_COLOR = (200, 50, 50)      # Red

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Define ranges for different keyboards
# Format: (Lowest MIDI Note, Highest MIDI Note)
KEYBOARD_RANGES = {
    '61': (36, 96),   # C2 to C7 (Standard 61-key)
    '88': (21, 108),  # A0 to C8 (Full Piano)
    '49': (48, 84)    # C3 to C6
}

# --- Helper Functions ---
def get_midi_input_name():
    """Finds a likely MIDI keyboard device."""
    input_names = mido.get_input_names()
    for name in input_names:
        if "Midi Through" not in name:
            return name
    return None

def midi_number_to_name(midi_num):
    """Converts 60 -> 'C4', 61 -> 'C#4', etc."""
    note_index = midi_num % 12
    octave = (midi_num // 12) - 1
    return f"{NOTE_NAMES[note_index]}{octave}"

def get_random_target_note(min_note, max_note):
    """Returns a random MIDI number within the user's keyboard range."""
    return random.randint(min_note, max_note)

# --- Main Game ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("OpenKeys: Note Trainer")
    
    # Fonts
    header_font = pygame.font.SysFont("arial", 60)
    main_font = pygame.font.SysFont("arial", 80)
    sub_font = pygame.font.SysFont("arial", 30)
    
    # MIDI Setup
    device_name = get_midi_input_name()
    if not device_name:
        print("No MIDI device found!")
        # We continue anyway so you can see the menu, but input won't work
    else:
        try:
            inport = mido.open_input(device_name)
        except OSError as e:
            print(f"Error: {e}")
            return

    # Game State Variables
    state = "MENU" # Can be "MENU" or "GAME"
    current_range = (36, 96) # Default to 61 keys
    
    # Game Logic Variables
    target_note_num = 0
    target_note_name = ""
    current_message = "Press the key!"
    feedback_color = TEXT_COLOR
    score = 0
    
    clock = pygame.time.Clock()
    running = True

    while running:
        # 1. Event Handling (Mouse & Keyboard)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Menu Selection Logic
            if state == "MENU" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_range = KEYBOARD_RANGES['61']
                    state = "GAME"
                    # Initialize first note
                    target_note_num = get_random_target_note(*current_range)
                    target_note_name = midi_number_to_name(target_note_num)
                elif event.key == pygame.K_2:
                    current_range = KEYBOARD_RANGES['88']
                    state = "GAME"
                    target_note_num = get_random_target_note(*current_range)
                    target_note_name = midi_number_to_name(target_note_num)
                elif event.key == pygame.K_3:
                    current_range = KEYBOARD_RANGES['49']
                    state = "GAME"
                    target_note_num = get_random_target_note(*current_range)
                    target_note_name = midi_number_to_name(target_note_num)

        # 2. MIDI Input Processing (Only if in GAME mode)
        if state == "GAME" and 'inport' in locals():
            for msg in inport.iter_pending():
                if msg.type == 'note_on' and msg.velocity > 0:
                    played_note_name = midi_number_to_name(msg.note)
                    
                    if msg.note == target_note_num:
                        current_message = f"Correct! ({played_note_name})"
                        feedback_color = SUCCESS_COLOR
                        score += 1
                        # Pick new note using the selected range
                        target_note_num = get_random_target_note(*current_range)
                        target_note_name = midi_number_to_name(target_note_num)
                    else:
                        current_message = f"Wrong: You pressed {played_note_name}"
                        feedback_color = FAIL_COLOR

        # 3. Drawing
        screen.fill(BG_COLOR)

        if state == "MENU":
            # Draw Menu
            title_text = header_font.render("Select Keyboard Size", True, ACCENT_COLOR)
            opt1 = sub_font.render("[1] 61 Keys (Standard Portable)", True, TEXT_COLOR)
            opt2 = sub_font.render("[2] 88 Keys (Full Piano)", True, TEXT_COLOR)
            opt3 = sub_font.render("[3] 49 Keys (Small)", True, TEXT_COLOR)
            
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))
            screen.blit(opt1, (WIDTH//2 - opt1.get_width()//2, 250))
            screen.blit(opt2, (WIDTH//2 - opt2.get_width()//2, 300))
            screen.blit(opt3, (WIDTH//2 - opt3.get_width()//2, 350))

        elif state == "GAME":
            # Draw Game
            target_text = main_font.render(f"Find: {target_note_name}", True, ACCENT_COLOR)
            target_rect = target_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            screen.blit(target_text, target_rect)

            feedback_text = sub_font.render(current_message, True, feedback_color)
            feedback_rect = feedback_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(feedback_text, feedback_rect)

            score_text = sub_font.render(f"Score: {score}", True, TEXT_COLOR)
            screen.blit(score_text, (20, 20))
            
            # Helper text to go back
            quit_text = sub_font.render("Press ESC to Quit", True, (100, 100, 100))
            screen.blit(quit_text, (WIDTH - 200, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(60)

    if 'inport' in locals():
        inport.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()