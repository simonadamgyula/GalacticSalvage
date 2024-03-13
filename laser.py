import random

import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], surface: pygame.Surface) -> None:
        super().__init__()
        self.warning = pygame.image.load("./img/laser/warning.png").convert_alpha()
        self.warning_rect = self.warning.get_rect(center=pos)
        self.pos = pos
        self.pos2 = (1600 - pos[0], pos[1])
        self.colors = [
            (255, 255, 255),
            (240, 218, 255),
            (240, 218, 255),
            (217, 162, 255),
            (217, 162, 255),
            (193, 103, 255),
            (183, 79, 255),
            (183, 79, 255),
        ]
        self.show_warning = False
        self.laser_go = False
        self.warning_timer = 0
        self.laser_go_timer = 0
        self.kill_rect = pygame.Rect((0, self.pos[1], 1600, 90)
        )


    def update(self, screen: pygame.Surface) -> None:
        self.draw_warning(screen)
        self.draw_laser(screen)

    def draw_warning(self, screen: pygame.Surface) -> None:
        if self.show_warning:
            screen.blit(self.warning, self.pos)
            screen.blit(self.warning, self.pos2)

    def draw_laser(self, screen: pygame.Surface) -> None:
        if self.laser_go:
            height = 90
            for color in self.colors:
                surface = pygame.Surface((1600, height), pygame.SRCALPHA)
                pygame.draw.rect(
                    surface, (*color, 100), pygame.Rect(0, 0, 1600, height)
                )
                screen.blit(surface, (0, self.pos[1]))
                height -= 10
        self.kill_rect = pygame.Rect((0, self.pos[1]-10, 1600, 70)
        )

    def get_pos(self) -> None:
        random_num = random.randint(100, 800)
        self.pos = (1475, random_num)
        self.pos2 = (25, self.pos[1])

    
