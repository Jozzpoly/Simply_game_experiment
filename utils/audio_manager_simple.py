import pygame
import os
from typing import Dict, Optional
from utils.constants import *

class AudioManager:
    """Simplified audio manager that avoids sound generation issues"""

    def __init__(self):
        # Initialize pygame mixer with safe settings
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Warning: Could not initialize audio: {e}")
            self.audio_enabled = False
            return

        self.audio_enabled = True

        # Volume settings
        self.master_volume: float = MASTER_VOLUME
        self.sfx_volume: float = SFX_VOLUME
        self.music_volume: float = MUSIC_VOLUME

        # Sound storage
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.current_music: Optional[str] = None
        self.music_playing: bool = False

        # Load sounds
        self._load_sounds()

        # Set initial volumes
        self._update_volumes()

    def _load_sounds(self) -> None:
        """Load all sound effects - simplified version"""
        if not self.audio_enabled:
            return

        sound_files = {
            'player_shoot': PLAYER_SHOOT_SOUND,
            'enemy_shoot': ENEMY_SHOOT_SOUND,
            'enemy_death': ENEMY_DEATH_SOUND,
            'item_collect': ITEM_COLLECT_SOUND,
            'level_up': LEVEL_UP_SOUND,
            'player_hurt': PLAYER_HURT_SOUND,
        }

        for sound_name, file_path in sound_files.items():
            try:
                if os.path.exists(file_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                else:
                    # Create a silent sound instead of generating audio
                    self.sounds[sound_name] = self._create_silent_sound()
            except pygame.error as e:
                print(f"Warning: Could not load sound {file_path}: {e}")
                # Create a silent sound as fallback
                self.sounds[sound_name] = self._create_silent_sound()

    def _create_silent_sound(self) -> pygame.mixer.Sound:
        """Create a minimal silent sound"""
        try:
            # Create a very short silent sound buffer
            buffer = b'\x00\x00' * 100  # Very short silent sound
            sound = pygame.mixer.Sound(buffer=buffer)
            return sound
        except Exception as e:
            print(f"Warning: Could not create silent sound: {e}")
            # Return a dummy sound object that won't crash the game
            class DummySound:
                def play(self): pass
                def set_volume(self, _): pass
                def stop(self): pass
            return DummySound()

    def _update_volumes(self) -> None:
        """Update all sound volumes based on current settings"""
        if not self.audio_enabled:
            return

        # Update sound effect volumes
        for sound in self.sounds.values():
            try:
                sound.set_volume(self.master_volume * self.sfx_volume)
            except:
                pass  # Ignore errors for dummy sounds

        # Update music volume
        try:
            pygame.mixer.music.set_volume(self.master_volume * self.music_volume)
        except:
            pass

    def play_sound(self, sound_name: str, volume_modifier: float = 1.0) -> None:
        """Play a sound effect"""
        if not self.audio_enabled or sound_name not in self.sounds:
            return

        try:
            sound = self.sounds[sound_name]
            sound.set_volume(self.master_volume * self.sfx_volume * volume_modifier)
            sound.play()
        except Exception as e:
            print(f"Warning: Could not play sound {sound_name}: {e}")

    def play_music(self, music_file: str, loop: bool = True) -> None:
        """Play background music"""
        if not self.audio_enabled:
            return

        try:
            if os.path.exists(music_file):
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play(-1 if loop else 0)
                self.current_music = music_file
                self.music_playing = True
            else:
                print(f"Warning: Music file {music_file} not found")
        except pygame.error as e:
            print(f"Warning: Could not play music {music_file}: {e}")

    def stop_music(self) -> None:
        """Stop background music"""
        if not self.audio_enabled:
            return
        try:
            pygame.mixer.music.stop()
            self.music_playing = False
            self.current_music = None
        except:
            pass

    def pause_music(self) -> None:
        """Pause background music"""
        if not self.audio_enabled:
            return
        try:
            pygame.mixer.music.pause()
        except:
            pass

    def resume_music(self) -> None:
        """Resume background music"""
        if not self.audio_enabled:
            return
        try:
            pygame.mixer.music.unpause()
        except:
            pass

    def set_master_volume(self, volume: float) -> None:
        """Set master volume (0.0 to 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_sfx_volume(self, volume: float) -> None:
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_music_volume(self, volume: float) -> None:
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def get_volumes(self) -> Dict[str, float]:
        """Get current volume settings"""
        return {
            'master': self.master_volume,
            'sfx': self.sfx_volume,
            'music': self.music_volume
        }

    def cleanup(self) -> None:
        """Clean up audio resources"""
        if not self.audio_enabled:
            return
        try:
            self.stop_music()
            pygame.mixer.quit()
        except:
            pass
