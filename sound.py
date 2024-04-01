import pygame


class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.music_index = 0
        self.game_music = "sound/game_music.mp3"
        self.menu_music = "sound/menu_music.mp3"
        self.all_music = [self.menu_music, self.game_music]
        self.music = pygame.mixer.music.load(self.all_music[self.music_index])

        self.laser = pygame.mixer.Sound("sound/laser.mp3")
        self.button = pygame.mixer.Sound("sound/button.mp3")
        self.explosion = pygame.mixer.Sound("sound/explosion.mp3")
        self.warning = pygame.mixer.Sound("sound/warning.mp3")
        self.wrong_button = pygame.mixer.Sound("sound/wrong_button.mp3")
        self.extend_arm = pygame.mixer.Sound("sound/extend_arm.mp3")
        self.collect = pygame.mixer.Sound("sound/collect.mp3")
        self.catch = pygame.mixer.Sound("sound/catch.mp3")

        self.enabled: bool = True

        self.all_sound = [
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
