import pygame


class Meteorite:
    def __init__(self, pos: pygame.Vector2, direction: float, speed: float) -> None:
        self.position: pygame.Vector2 = pos
        self.direction: float = direction
        self.velocity: float = speed

        self.rotation_speed: float = 0
        self.rotation: float = 0

        self.image: pygame.Surface = pygame.Surface((100, 100))
        pygame.draw.circle(self.image, "yellow", (50, 50), 50)

    def rotate(self) -> None:
        self.rotation += self.rotation_speed
        self.rotation %= 360

    def draw(self, screen: pygame.Surface) -> None:
        rotated_image: pygame.Surface = pygame.transform.rotate(self.image, self.direction)
        rotated_rect: pygame.Rect = rotated_image.get_rect(center=self.image.get_rect(center=self.position).center)

        screen.blit(rotated_image, rotated_rect.topleft)


