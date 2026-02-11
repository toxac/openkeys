# core/scene_manager.py
from scenes.menu_scene import MenuScene
from scenes.note_trainer import NoteTrainerScene # <-- Import the new scene

class SceneManager:
    def __init__(self):
        self.active_scene = MenuScene(self)
    
    def switch_to(self, scene_name):
        if scene_name == 'MENU':
            self.active_scene = MenuScene(self)
        elif scene_name == 'NOTE_TRAINER': # <-- Add this check
            self.active_scene = NoteTrainerScene(self)
    
    def get_active_scene(self):
        return self.active_scene