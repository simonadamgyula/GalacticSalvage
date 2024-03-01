import pygame
import math

from grabber import Grabber
from meteorite import Meteorite


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

    def draw(self, screen: pygame.Surface) -> None:
        self.grabber.draw(screen)

        rotated_image: pygame.Surface = pygame.transform.rotate(self.image, self.direction)
        self.rotated_rect = rotated_image.get_rect(center=self.image.get_rect(center=self.position).center)

        screen.blit(rotated_image, self.rotated_rect.topleft)

    def update(self, meteorites: list[Meteorite]) -> bool:
        self.animate()
        self.move()
        self.grabber.update(self.position)
        return self.check_collision(meteorites)

    def accelerate(self) -> None:
        acceleration: pygame.Vector2 = pygame.Vector2(
            math.sin(math.radians(self.direction)),
            math.cos(math.radians(self.direction))
        ) * self.acceleration

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

    def check_collision(self, meteorites: list[Meteorite]) -> bool:
        for meteorite in meteorites:
            closest_x = clamp(meteorite.position.x, self.rotated_rect.left, self.rotated_rect.right)
            closest_y = clamp(meteorite.position.y, self.rotated_rect.top, self.rotated_rect.bottom)

            distance_x: float = meteorite.position.x - closest_x
            distance_y: float = meteorite.position.y - closest_y

            distance_squared: float = distance_x ** 2 + distance_y ** 2
            if distance_squared < meteorite.radius ** 2:
                return True

        return False
