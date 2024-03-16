import random

import pygame


from typing import List, Tuple
import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int], surface: pygame.Surface) -> None:
        super().__init__()
        self.warning = pygame.image.load("./img/laser/warning.png").convert_alpha()
        self.warning_rect = self.warning.get_rect(center=pos)

        self.pos: Tuple[int, int] = pos
        self.pos2: Tuple[int, int] = (1600 - pos[0], pos[1])
        self.pos_ver: Tuple[int, int] = pos
        self.pos2_ver: Tuple[int, int] = (pos[0], 900 - self.pos_ver[1])

        self.direction: int = 1
        
        self.random_color: int = 1
        self.colors: List[List[Tuple[int, int, int]]] = [
            # piros
            [
                (255, 231, 231),
                (255, 226, 226),
                (255, 196, 196),
                (255, 167, 167),
                (255, 134, 134),
                (255, 81, 81),
                (254, 46, 46),
                (255, 16, 16),
            ],
            # lila
            [
                (251, 231, 255),
                (240, 218, 255),
                (226, 183, 255),
                (211, 147, 255),
                (198, 115, 255),
                (183, 77, 255),
                (170, 46, 255),
                (157, 14, 255),
            ],
            # zöld
            [
                (223, 255, 241),
                (215, 255, 237),
                (183, 254, 222),
                (148, 255, 206),
                (108, 255, 188),
                (108, 255, 188),
                (38, 255, 156),
                (38, 255, 156),
            ],
        ]
        self.show_warning: bool = False
        self.laser_go: bool = False

        self.kill_rect: pygame.Rect = pygame.Rect((0, self.pos[1], 1600, 90))
        self.kill_rect_ver: pygame.Rect = pygame.Rect((self.pos_ver[0] - 10, 0, 70, 900))

        self.two_laser: bool = False
        self.all_laser: int = 0

        self.enabled: bool = False


    def update(self, screen: pygame.Surface) -> None:
        if self.two_laser:
            self.draw_laser(screen)
            self.draw_warning(screen)  
            self.draw_laser_ver(screen)
            self.draw_warning_ver(screen)
        else:
            if self.direction == 1:
                self.draw_laser(screen)
                self.draw_warning(screen)            
            else:
                self.draw_laser_ver(screen)
                self.draw_warning_ver(screen)

    def draw_warning(self, screen: pygame.Surface) -> None:
        if self.show_warning:
            screen.blit(self.warning, self.pos)
            screen.blit(self.warning, self.pos2)

    def draw_warning_ver(self, screen: pygame.Surface) -> None:
        if self.show_warning:
            screen.blit(self.warning, self.pos_ver)
            screen.blit(self.warning, self.pos2_ver)

    def draw_laser(self, screen: pygame.Surface) -> None:
        if self.laser_go:
            height: int = 80
            pos: int = self.pos[1]
            for color in self.colors[self.random_color][::-1]:
                surface: pygame.Surface = pygame.Surface((1600, height), pygame.SRCALPHA)
                pygame.draw.rect(
                    surface, (*color, 100), pygame.Rect(0, 0, 1600, height)
                )
                screen.blit(surface, (0, pos))
                pos += 5
                height -= 10
        self.kill_rect: pygame.Rect = pygame.Rect((0, self.pos[1] - 10, 1600, 55))

    def draw_laser_ver(self, screen: pygame.Surface) -> None:
        if self.laser_go:
            width: int = 80
            pos: int = self.pos_ver[0]
            for color in self.colors[self.random_color][::-1]:
                surface: pygame.Surface = pygame.Surface((width, 900), pygame.SRCALPHA)
                pygame.draw.rect(surface, (*color, 100), pygame.Rect(0, 0, width, 900))
                screen.blit(surface, (pos, 0))
                pos += 5
                width -= 10
        self.kill_rect_ver: pygame.Rect = pygame.Rect((self.pos_ver[0] - 10, 0, 70, 900))

    def get_pos(self) -> None:
        self.direction: int = random.randint(1, 2)
        self.random_color: int = random.randint(0, 2)
        if self.direction == 1:
            random_num: int = random.randint(100, 800)
            self.pos: Tuple[int,int] = (1475, random_num)
            self.pos2: Tuple[int,int] = (25, self.pos[1])
        else:
            random_num: int = random.randint(100, 1500)
            self.pos_ver: Tuple[int,int] = (random_num, 25)
            self.pos2_ver: Tuple[int,int] = (random_num, 775)

    

