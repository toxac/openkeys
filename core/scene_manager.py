# core/scene_manager.py
from scenes.menu_scene import MenuScene
from scenes.note_trainer import NoteTrainerScene
from scenes.rhythm_trainer import RhythmTrainerScene # <-- 1. Import it

class SceneManager:
    def __init__(self):
        self.active_scene = MenuScene(self)
    
    def switch_to(self, scene_name):
        if scene_name == 'MENU':
            self.active_scene = MenuScene(self)
        elif scene_name == 'NOTE_TRAINER':
            self.active_scene = NoteTrainerScene(self)
        elif scene_name == 'RHYTHM_TRAINER': # <-- 2. Add this
            self.active_scene = RhythmTrainerScene(self)
    
    def get_active_scene(self):
        return self.active_scene