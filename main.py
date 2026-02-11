# main.py
import pygame
import mido
import sys
from config import *
from core.scene_manager import SceneManager

def get_midi_input():
    try:
        names = mido.get_input_names()
        for name in names:
            if "Midi Through" not in name:
                print(f"Connected to MIDI: {name}")
                return mido.open_input(name)
    except Exception as e:
        print(f"MIDI Error: {e}")
    return None

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("OpenKeys")
    clock = pygame.time.Clock()

    # Initialize Systems
    scene_manager = SceneManager()
    midi_in = get_midi_input()

    running = True
    while running:
        # 1. Collect Inputs
        pygame_events = pygame.event.get()
        midi_messages = []
        
        # Get Pygame Quit Event
        for event in pygame_events:
            if event.type == pygame.QUIT:
                running = False
        
        # Get MIDI Messages (Non-blocking)
        if midi_in:
            for msg in midi_in.iter_pending():
                midi_messages.append(msg)

        # 2. Update Active Scene
        current_scene = scene_manager.get_active_scene()
        
        current_scene.handle_input(pygame_events)
        current_scene.process_midi(midi_messages)
        current_scene.update()

        # 3. Draw Active Scene
        current_scene.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

    if midi_in:
        midi_in.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()