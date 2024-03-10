import typing
import random
import pygame

from meteorite import Meteorite


class Debris(pygame.sprite.Sprite):
    debris_group: pygame.sprite.Group = pygame.sprite.Group()  # type: ignore

    def __init__(self, pos: pygame.Vector2, direction: float, speed: float) -> None:
        super().__init__()

        self.position: pygame.Vector2 = pos
        self.direction: float = direction
        self.velocity: float = speed

        self.rotation_speed: float = 0.5
        self.rotation: float = 0

        self.image: pygame.Surface = pygame.image.load("./img/debris/satellite.png")

        self.caught: bool = False

    def update(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        screen: pygame.Surface = kwargs["screen"]

        self.rotate()

        if not self.caught:
            self.move()
        self.check_outside(screen.get_size())

        self.draw(screen)

    def draw(self, screen: pygame.Surface) -> None:
        rotated_image: pygame.Surface = pygame.transform.rotate(self.image, self.rotation)
        rotated_rect: pygame.Rect = rotated_image.get_rect(center=self.image.get_rect(center=self.position).center)

        screen.blit(rotated_image, rotated_rect.topleft)

    def rotate(self) -> None:
        self.rotation += self.rotation_speed
        self.rotation %= 360

    def move(self) -> None:
        self.position += pygame.Vector2(0, 1).rotate(-self.direction) * self.velocity

    def snap(self, position: pygame.Vector2) -> None:
        self.position = position

    def check_outside(self, screen_resolution: tuple[int, int]) -> None:
        if self.position.x < -40 or self.position.x > screen_resolution[0] + 40 or \
                self.position.y < -40 or self.position.y > screen_resolution[1] + 40:
            self.kill()

    @staticmethod
    def create_random(screen_resolution: tuple[int, int]) -> None:
        position: pygame.Vector2 = Meteorite.generate_point_outside_screen(screen_resolution, 20)
        direction: float = Meteorite.create_random_direction(screen_resolution, position)
        speed: float = random.random() * 2 + 1

        Debris.debris_group.add(Debris(position, direction, speed))  # type: ignore
