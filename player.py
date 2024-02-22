import pygame
import math


class Player:
    def __init__(self, x: int, y: int, direction: float) -> None:
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.direction: float = direction

        self.rotation_speed: float = 2

        self.speed: float = 0
        self.acceleration: float = 0.5
        self.deceleration: float = 0.1
        self.max_velocity: float = 5

        self.image: pygame.Surface = pygame.image.load("img/spaceship/placeholder.png").convert_alpha()

    def draw(self, screen: pygame.Surface) -> None:
        rotated_image: pygame.Surface = pygame.transform.rotate(self.image, self.direction)
        rotated_rect: pygame.Rect = rotated_image.get_rect(center=self.image.get_rect(center=self.position).center)

        screen.blit(rotated_image, rotated_rect.topleft)

    def update(self, screen: pygame.Surface, move: bool = False) -> None:
        self.accelerate(move)
        self.move()
        self.draw(screen)

    def accelerate(self, accelerate: bool = False) -> None:
        self.speed += self.acceleration if accelerate else -self.deceleration

        if self.speed > self.max_velocity:

            self.speed = self.max_velocity
        elif self.speed < 0:
            self.speed = 0

    def move(self) -> None:
        self.position -= pygame.Vector2(
            math.sin(math.radians(self.direction)) * self.speed,
            math.cos(math.radians(self.direction)) * self.speed
        )

    def rotate(self, direction: float) -> None:
        self.direction += direction * self.rotation_speed
        self.direction %= 360
