import pygame


class Animation:
    def __init__(self, images: list[pygame.Surface], animation_speed: float, repeating: bool = True) -> None:
        self.images: list[pygame.Surface] = images
        self.animation_speed: float = animation_speed
        self.length = len(images)
        self.index: float = 0
        self.repeating: bool = repeating

    def next(self) -> pygame.Surface | None:
        self.index += self.animation_speed

        if not self.repeating and self.index >= self.length:
            return None
        self.index %= self.length

        return self.images[int(self.index)]

    def draw_next(self, screen: pygame.Surface, position: pygame.Vector2) -> None:
        image: pygame.Surface | None = self.next()

        if image is not None:
            rect: pygame.Rect = image.get_rect(center=position)
            screen.blit(image, rect)

    def reset(self) -> None:
        self.index = 0

    @staticmethod
    def import_spritesheet(file_path: str, width: int, height: int,
                           animation_speed: float, repeating: bool = True) -> "Animation":
        sprite_sheet: pygame.Surface = pygame.image.load(file_path).convert_alpha()

        images: list[pygame.Surface] = []
        for i in range(sprite_sheet.get_width() // width):
            current_image: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            source_rect: pygame.Rect = pygame.Rect(i * width, 0, width, height)
            current_image.blit(sprite_sheet, (0, 0), source_rect)
            images.append(current_image)

        return Animation(images, animation_speed, repeating)
