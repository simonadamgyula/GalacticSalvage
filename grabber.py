import math
import pygame


class Grabber:
    def __init__(self, position: pygame.Vector2) -> None:
        self.position: pygame.Vector2 = position
        self.direction: float = 0

        self.image = pygame.image.load("img/grabber/placeholder.png").convert_alpha()

    def update(self, position: pygame.Vector2, screen: pygame.Surface) -> None:
        self.move(position)
        self.rotate()
        self.draw(screen)

    def move(self, position: pygame.Vector2) -> None:
        self.position = position

    def rotate(self) -> None:
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        mouse_vec: pygame.Vector2 = pygame.Vector2(mouse_pos[0] - self.position.x, mouse_pos[1] - self.position.y)

        self.direction = math.degrees(math.atan2(mouse_vec.x, mouse_vec.y))

    def draw(self, screen: pygame.Surface) -> None:
        rotated_image, rotated_image_rect = self.get_rotated_image()

        screen.blit(rotated_image, rotated_image_rect)

    def get_rotated_image(self) -> tuple[pygame.Surface, pygame.Rect]:
        image_rect = self.image.get_rect(center=(self.position.x, self.position.y))
        offset_center_to_pivot = pygame.math.Vector2(self.position) - image_rect.midbottom

        rotated_offset = offset_center_to_pivot.rotate(-self.direction)

        rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)

        rotated_image = pygame.transform.rotate(self.image, self.direction)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        return rotated_image, rotated_image_rect
