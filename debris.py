import pygame
import random
import math


class Debris(pygame.sprite.Sprite):
    debris_group: pygame.sprite.Group = pygame.sprite.Group()

    def __init__(self, pos: pygame.Vector2, direction: float, speed: float) -> None:
        super().__init__()

        self.position: pygame.Vector2 = pos
        self.direction: float = direction
        self.velocity: float = speed

        self.rotation_speed: float = 0.1
        self.rotation: float = 0

    def update(self, *args, **kwargs) -> None:
        screen: pygame.Surface = kwargs["screen"]

        self.rotate()
        self.move()
        self.check_outside(screen.get_size())

        self.draw(screen)

    def draw(self, screen: pygame.Surface) -> None:
        # not permanent, just for testing
        pygame.draw.circle(screen, "yellow", self.position, 10)

    def rotate(self) -> None:
        self.rotation += self.rotation_speed

    def move(self) -> None:
        self.position += pygame.Vector2(0, 1).rotate(-self.direction) * self.velocity

    def check_outside(self, screen_resolution: tuple[int, int]) -> None:
        if self.position.x < -20 or self.position.x > screen_resolution[0] + 20 or \
                self.position.y < -20 or self.position.y > screen_resolution[1] + 20:
            self.kill()

    @staticmethod
    def create_random(screen_resolution: tuple[int, int]) -> None:
        position: pygame.Vector2 = Debris.generate_point_outside_screen(screen_resolution)
        direction: float = Debris.create_random_direction(screen_resolution, position)
        speed: float = random.random() * 2 + 1

        Debris.debris_group.add(Debris(position, direction, speed))

    @staticmethod
    def create_random_direction(screen_resolution: tuple[int, int], position: pygame.Vector2) -> float:
        point: pygame.Vector2 = pygame.Vector2(random.randint(50, screen_resolution[0] - 50),
                                               random.randint(50, screen_resolution[1] - 50))

        return math.degrees(math.atan2(point.x - position.x, point.y - position.y))

    @staticmethod
    def generate_point_outside_screen(screen_resolution: tuple[int, int]):
        bounding_width: int = screen_resolution[0] + 20
        bounding_height: int = screen_resolution[1] + 20

        position: pygame.Vector2 = pygame.Vector2(0, 0)

        p = random.randint(0, (bounding_width + bounding_height) * 2)
        if p < (bounding_width + bounding_height):
            if p < bounding_width:
                position.x = p
                position.y = 0
            else:
                position.x = bounding_width
                position.y = p - bounding_width
        else:
            p = p - (bounding_width + bounding_height)
            if p < bounding_width:
                position.x = bounding_width - p
                position.y = bounding_height
            else:
                position.x = 0
                position.y = bounding_height - (p - bounding_width)

        position.x -= 10
        position.y -= 10

        return position
