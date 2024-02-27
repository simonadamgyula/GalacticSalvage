import pygame
import math


class Player:
    def __init__(self, x: int, y: int, direction: float) -> None:
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.direction: float = direction

        self.rotation_speed: float = 2

        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.acceleration: float = 0.5
        self.max_velocity: float = 3

        self.image: pygame.Surface = pygame.image.load("img/spaceship/placeholder.png").convert_alpha()

    def draw(self, screen: pygame.Surface) -> None:
        rotated_image: pygame.Surface = pygame.transform.rotate(self.image, self.direction)
        rotated_rect: pygame.Rect = rotated_image.get_rect(center=self.image.get_rect(center=self.position).center)

        screen.blit(rotated_image, rotated_rect.topleft)

    def update(self, screen: pygame.Surface) -> None:
        self.move()
        self.draw(screen)

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
