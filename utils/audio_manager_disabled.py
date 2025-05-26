"""
Disabled audio manager - no sound functionality
Use this if you have audio issues and just want to run the game
"""

from typing import Dict

class AudioManager:
    """Disabled audio manager that provides all methods but no actual audio"""

    def __init__(self):
        print("Audio disabled - running in silent mode")
        self.master_volume = 0.7
        self.sfx_volume = 0.8
        self.music_volume = 0.6
        self.sounds = {}
        self.current_music = None
        self.music_playing = False

    def _load_sounds(self) -> None:
        """Dummy method - no sounds loaded"""
        pass

    def _update_volumes(self) -> None:
        """Dummy method - no volume updates"""
        pass

    def play_sound(self, sound_name: str, volume_modifier: float = 1.0) -> None:
        """Dummy method - no sound played"""
        pass

    def play_music(self, music_file: str, loop: bool = True) -> None:
        """Dummy method - no music played"""
        pass

    def stop_music(self) -> None:
        """Dummy method - no music to stop"""
        pass

    def pause_music(self) -> None:
        """Dummy method - no music to pause"""
        pass

    def resume_music(self) -> None:
        """Dummy method - no music to resume"""
        pass

    def set_master_volume(self, volume: float) -> None:
        """Set master volume (dummy)"""
        self.master_volume = max(0.0, min(1.0, volume))

    def set_sfx_volume(self, volume: float) -> None:
        """Set sound effects volume (dummy)"""
        self.sfx_volume = max(0.0, min(1.0, volume))

    def set_music_volume(self, volume: float) -> None:
        """Set music volume (dummy)"""
        self.music_volume = max(0.0, min(1.0, volume))

    def get_volumes(self) -> Dict[str, float]:
        """Get current volume settings"""
        return {
            'master': self.master_volume,
            'sfx': self.sfx_volume,
            'music': self.music_volume
        }

    def cleanup(self) -> None:
        """Dummy cleanup method"""
        pass
