from typing import List, Any

import pygame


class Sound:
    __instance: Any = None

    def __new__(cls) -> "Sound":
        if cls.__instance is None:
            cls.__instance = super(Sound, cls).__new__(cls)
            return cls.__instance
        return cls.__instance

    def __init__(self) -> None:
        pygame.mixer.init()
        self.music_index: int = 0
        self.game_music: str = "sound/game_music.mp3"
        self.menu_music: str = "sound/menu_music.mp3"
        self.all_music: List[str] = [self.menu_music, self.game_music]
        self.music = pygame.mixer.music.load(self.all_music[self.music_index])

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

    def music_index_controll(self) -> None:
        if self.music_index > 1:
            self.music_index = 0

    def controll_volume(self) -> None:
        if self.enabled:
            pygame.mixer.music.set_volume(0.3)
        else:
            pygame.mixer.music.set_volume(0)

    def play_sound(self, sound: pygame.mixer.Sound) -> None:
        if self.enabled:
            sound.play()
