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

    def music_index_controll(self) -> None:
        if self.music_index > 1:
            self.music_index = 0
