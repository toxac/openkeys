# scenes/base_scene.py
class BaseScene:
    def __init__(self, manager):
        self.manager = manager  # Reference to the SceneManager to switch scenes

    def handle_input(self, events):
        """Handle keyboard/mouse events (Pygame events)."""
        pass

    def process_midi(self, midi_messages):
        """Handle incoming MIDI messages (List of mido messages)."""
        pass

    def update(self):
        """Game logic updates (timers, physics, etc)."""
        pass

    def draw(self, screen):
        """Render everything to the screen."""
        pass