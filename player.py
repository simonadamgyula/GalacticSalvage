import pygame
import math

from grabber import Grabber


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

        self.grabber: Grabber = Grabber(self.position)

    def draw(self, screen: pygame.Surface) -> None:
        self.grabber.draw(screen)

        rotated_image: pygame.Surface = pygame.transform.rotate(self.image, self.direction)
        rotated_rect: pygame.Rect = rotated_image.get_rect(center=self.image.get_rect(center=self.position).center)

        screen.blit(rotated_image, rotated_rect.topleft)

    def update(self, screen: pygame.Surface) -> None:
        self.animate()
        self.move()
        self.grabber.update(self.position)

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
