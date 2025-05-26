import pygame
import os
from typing import Dict, Optional
from utils.constants import *

class AudioManager:
    """Manages all audio for the game including sound effects and music"""

    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()

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
        """Load all sound effects"""
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
                    # Create a simple placeholder sound if file doesn't exist
                    self.sounds[sound_name] = self._create_placeholder_sound(sound_name)
            except pygame.error as e:
                print(f"Warning: Could not load sound {file_path}: {e}")
                # Create a placeholder sound
                try:
                    self.sounds[sound_name] = self._create_placeholder_sound(sound_name)
                except Exception as placeholder_error:
                    print(f"Warning: Could not create placeholder sound for {sound_name}: {placeholder_error}")
                    # Create a minimal silent sound as last resort
                    self.sounds[sound_name] = self._create_silent_sound()

    def _create_placeholder_sound(self, sound_name: str) -> pygame.mixer.Sound:
        """Create a simple placeholder sound using pygame's built-in sound generation"""
        # Create a simple beep sound as placeholder
        sample_rate = 22050
        duration = 0.1  # 100ms

        if sound_name == 'player_shoot':
            frequency = 800
        elif sound_name == 'enemy_shoot':
            frequency = 600
        elif sound_name == 'enemy_death':
            frequency = 200
            duration = 0.3
        elif sound_name == 'item_collect':
            frequency = 1000
        elif sound_name == 'level_up':
            frequency = 1200
            duration = 0.5
        elif sound_name == 'player_hurt':
            frequency = 300
            duration = 0.2
        else:
            frequency = 440

        # Generate a simple sine wave using built-in math
        import math
        frames = int(duration * sample_rate)
        arr = []

        for i in range(frames):
            time = float(i) / sample_rate
            wave = math.sin(frequency * 2 * math.pi * time)
            # Apply envelope to avoid clicks
            envelope = min(1.0, 4.0 * time) * min(1.0, 4.0 * (duration - time))
            sample = int(wave * envelope * 0.3 * 32767)
            arr.append([sample, sample])  # Stereo

        # Convert to pygame sound
        try:
            import pygame.sndarray
            import numpy as np

            # Get mixer configuration to match array format
            _, _, mixer_channels = pygame.mixer.get_init()

            # Create array with correct shape based on mixer channels
            if mixer_channels == 1:  # Mono
                # Convert stereo array to mono
                arr_mono = []
                for sample_pair in arr:
                    arr_mono.append(sample_pair[0])  # Take left channel
                arr_np = np.array(arr_mono, dtype=np.int16)
            else:  # Stereo or more channels
                arr_np = np.array(arr, dtype=np.int16)

            sound = pygame.sndarray.make_sound(arr_np)
            return sound

        except (ImportError, ValueError) as e:
            print(f"Warning: Could not create advanced sound for {sound_name}: {e}")
            # Fallback: create a very simple silent sound buffer
            try:
                # Get mixer configuration for proper buffer size
                _, _, mixer_channels = pygame.mixer.get_init()

                # Create silent buffer with correct format
                if mixer_channels == 1:  # Mono
                    buffer = b'\x00\x00' * frames
                else:  # Stereo
                    buffer = b'\x00\x00\x00\x00' * frames

                sound = pygame.mixer.Sound(buffer=buffer)
                return sound
            except Exception as fallback_error:
                print(f"Warning: Could not create fallback sound: {fallback_error}")
                # Create the most basic sound possible
                buffer = b'\x00\x00' * 1000  # Very short silent sound
                sound = pygame.mixer.Sound(buffer=buffer)
                return sound

    def _create_silent_sound(self) -> pygame.mixer.Sound:
        """Create a minimal silent sound as absolute fallback"""
        try:
            # Create the most basic silent sound possible
            buffer = b'\x00\x00' * 1000  # Very short silent sound
            sound = pygame.mixer.Sound(buffer=buffer)
            return sound
        except Exception as e:
            print(f"Critical: Could not create even a silent sound: {e}")
            # This should never happen, but if it does, we'll create an empty sound object
            # that won't crash the game
            class DummySound:
                def play(self): pass
                def set_volume(self, _): pass  # Ignore volume parameter
                def stop(self): pass
            return DummySound()

    def _update_volumes(self) -> None:
        """Update all sound volumes based on current settings"""
        # Update sound effect volumes
        for sound in self.sounds.values():
            sound.set_volume(self.master_volume * self.sfx_volume)

        # Update music volume
        pygame.mixer.music.set_volume(self.master_volume * self.music_volume)

    def play_sound(self, sound_name: str, volume_modifier: float = 1.0) -> None:
        """Play a sound effect"""
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            # Create a copy to avoid conflicts with volume changes
            sound_copy = sound
            sound_copy.set_volume(self.master_volume * self.sfx_volume * volume_modifier)
            sound_copy.play()

    def play_music(self, music_file: str, loop: bool = True) -> None:
        """Play background music"""
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
        pygame.mixer.music.stop()
        self.music_playing = False
        self.current_music = None

    def pause_music(self) -> None:
        """Pause background music"""
        pygame.mixer.music.pause()

    def resume_music(self) -> None:
        """Resume background music"""
        pygame.mixer.music.unpause()

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
        self.stop_music()
        pygame.mixer.quit()
