from typing import List, Any

import pygame


class Sound(object):
    _instance: Any = None
    _initialized: bool = False

    def __new__(cls, *args: Any, **kwargs: Any) -> "Sound":
        if cls._instance is None:
            cls._instance = super(Sound, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True

        pygame.mixer.init()
        self.music_index: int = 0
        self.game_music: str = "sound/game_music.mp3"
        self.menu_music: str = "sound/menu_music.mp3"
        self.all_music: List[str] = [self.menu_music, self.game_music]
        pygame.mixer.music.load(self.all_music[self.music_index])

        self.laser: pygame.mixer.Sound = pygame.mixer.Sound("sound/laser.mp3")
        self.button: pygame.mixer.Sound = pygame.mixer.Sound("sound/button.mp3")
        self.explosion: pygame.mixer.Sound = pygame.mixer.Sound("sound/explosion.mp3")
        self.warning: pygame.mixer.Sound = pygame.mixer.Sound("sound/warning.mp3")
        self.wrong_button: pygame.mixer.Sound = pygame.mixer.Sound(
            "sound/wrong_button.mp3"
        )
        self.extend_arm: pygame.mixer.Sound = pygame.mixer.Sound("sound/extend_arm.mp3")
        self.collect: pygame.mixer.Sound = pygame.mixer.Sound("sound/collect.mp3")
        self.catch: pygame.mixer.Sound = pygame.mixer.Sound("sound/catch.mp3")

        self.enabled: bool = True
        self._music_enabled: bool = True

        self.all_sound: List[pygame.mixer.Sound] = [
            self.laser,
            self.button,
            self.explosion,
            self.warning,
            self.wrong_button,
            self.extend_arm,
            self.collect,
            self.catch,
        ]

    @property
    def music_enabled(self) -> bool:
        return self._music_enabled

    @music_enabled.setter
    def music_enabled(self, value: bool) -> None:
        self._music_enabled = value
        self.controll_volume()

    def music_index_controll(self) -> None:
        if self.music_index > 1:
            self.music_index = 0

    def controll_volume(self) -> None:
        if self._music_enabled:
            pygame.mixer.music.set_volume(0.3)
        else:
            pygame.mixer.music.set_volume(0)

    def play_sound(self, sound: pygame.mixer.Sound) -> None:
        if self.enabled:
            sound.play()
