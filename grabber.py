import math
import pygame
from enum import Enum


class ExtensionStage(Enum):
    STOPPED: int = 0
    EXTENDING: int = 1
    RETRACTING: int = 2


class Grabber:
    def __init__(self, position: pygame.Vector2) -> None:
        self.position: pygame.Vector2 = position
        self.direction: float = 0

        self.extension_stage: ExtensionStage = ExtensionStage.STOPPED
        self.extension_speed: int = 5
        self.length: int = 0

        self.image = pygame.image.load("img/grabber/placeholder3.png").convert_alpha()

        self.max_length: int = self.image.get_height()

    def extend(self) -> None:
        if self.extension_stage != ExtensionStage.STOPPED:
            return

        self.rotate()
        self.extension_stage = ExtensionStage.EXTENDING

    def update(self, position: pygame.Vector2) -> None:
        self.move(position)
        self.extension()

    def move(self, position: pygame.Vector2) -> None:
        self.position = position

    def extension(self) -> None:
        if self.extension_stage == ExtensionStage.STOPPED:
            return

        if self.extension_stage == ExtensionStage.EXTENDING:
            self.length += self.extension_speed
        elif self.extension_stage == ExtensionStage.RETRACTING:
            self.length -= self.extension_speed

        if self.length < 0:
            self.length = 0
            self.extension_stage = ExtensionStage.STOPPED
        if self.length > self.max_length:
            self.length = self.max_length
            self.extension_stage = ExtensionStage.RETRACTING

    def rotate(self) -> None:
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        mouse_vec: pygame.Vector2 = pygame.Vector2(mouse_pos[0] - self.position.x, mouse_pos[1] - self.position.y)

        self.direction = math.degrees(math.atan2(mouse_vec.x, mouse_vec.y))

    def draw(self, screen: pygame.Surface) -> None:
        chopped_image: pygame.Surface = self.chop_image(self.max_length - self.length)
        rotated_image, rotated_image_rect = self.get_rotated_image(chopped_image)

        screen.blit(rotated_image, rotated_image_rect)

    def chop_image(self, height: int) -> pygame.Surface:
        chop_rect: pygame.Rect = pygame.Rect(0, height, self.image.get_width(), self.image.get_height() - height)
        chopped_image: pygame.Surface = self.image.subsurface(chop_rect)

        return chopped_image

    def get_rotated_image(self, image: pygame.Surface) -> tuple[pygame.Surface, pygame.Rect]:
        image_rect = image.get_rect(center=(self.position.x, self.position.y))
        offset_center_to_pivot = pygame.math.Vector2(self.position) - image_rect.midbottom

        rotated_offset = offset_center_to_pivot.rotate(-self.direction)

        rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)

        rotated_image = pygame.transform.rotate(image, self.direction)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        return rotated_image, rotated_image_rect
