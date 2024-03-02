import pygame
import math

from grabber import Grabber
from meteorite import Meteorite
from collision import Collision


def clamp(value: float, min_: float, max_: float) -> float:
    return max(min(value, max_), min_)


class Player:
    def __init__(self, x: int, y: int, direction: float) -> None:
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.direction: float = direction

        self.rotation_speed: float = 2

        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.acceleration: float = 0.5
        self.max_velocity: float = 3

        self.images: list[pygame.Surface] = []
        self.images.append(pygame.image.load("img/spaceship/1.png"))
        self.images.append(pygame.image.load("img/spaceship/2.png"))
        self.images.append(pygame.image.load("img/spaceship/3.png"))
        self.images.append(pygame.image.load("img/spaceship/4.png"))
        self.images.append(pygame.image.load("img/spaceship/5.png"))
        self.frame_index = 0
        self.animation_speed: float = 0.3

        self.image: pygame.Surface = self.images[self.frame_index]
        self.rotated_rect: pygame.Rect = self.image.get_rect(center=(0, 0))

        self.grabber: Grabber = Grabber(self.position)

    @property
    def resolution(self) -> tuple[int, int]:
        return self.image.get_width(), self.image.get_height()

    def draw(self, screen: pygame.Surface, collision: bool) -> None:
        self.grabber.draw(screen)

        rotated_image: pygame.Surface = pygame.transform.rotate(self.image, self.direction)
        self.rotated_rect = rotated_image.get_rect(center=self.image.get_rect(center=self.position).center)

        screen.blit(rotated_image, self.rotated_rect.topleft)

        if not collision:
            return

        pygame.draw.circle(screen, "red", self.position,
                           math.sqrt((self.image.get_width() / 2) ** 2 + (self.image.get_height() / 2) ** 2), 1)

    def update(self) -> None:
        self.animate()
        self.move()
        self.grabber.update(self.position)

    def accelerate(self) -> None:
        acceleration: pygame.Vector2 = pygame.Vector2(0, 1).rotate(-self.direction) * self.acceleration

        self.velocity += acceleration
        self.velocity = self.velocity.clamp_magnitude(self.max_velocity)

    def move(self) -> None:
        self.position -= self.velocity

    def rotate(self, direction: float) -> None:
        self.direction += direction * self.rotation_speed
        self.direction %= 360

    def animate(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.images):
            self.frame_index = 0

        self.image = self.images[int(self.frame_index)]

    def get_verticies(self) -> list[pygame.Vector2]:
        width: int = self.image.get_width()
        height: int = self.image.get_height()

        verticies: list[pygame.Vector2] = []
        for i in range(4):
            binary: str = format(i, 'b').zfill(2)
            verticies.append(pygame.Vector2((width / 2) * (1 if binary[0] == '0' else -1),
                                            (height / 2) * (1 if binary[1] == '0' else -1))
                             .rotate(-self.direction) + self.position)

        verticies[-1], verticies[-2] = verticies[-2], verticies[-1]
        return verticies

    def check_collision(self, meteorites: list[Meteorite]) -> bool:
        verticies: list[pygame.Vector2] = self.get_verticies()
        for meteorite in meteorites:
            if (meteorite.radius + math.sqrt((self.image.get_width() / 2) ** 2 + (self.image.get_height() / 2) ** 2) <
                    (self.position - meteorite.position).magnitude()):
                continue

            if Collision.rectangle_circle_collision(self.position, verticies, meteorite.position, meteorite.radius):
                return True

        return False
