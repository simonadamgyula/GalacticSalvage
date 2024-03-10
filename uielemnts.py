import typing

from collections.abc import Callable
import pygame


class Button:
    def __init__(self, size: tuple[int, int], position: tuple[int, int], text: str, font: pygame.font.Font,
                 color: tuple[int, int, int] | str, font_color: tuple[int, int, int] | str, function: Callable[[], typing.Any],
                 active: Callable[[], bool] = lambda: True) -> None:
        self.surface: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
        self.surface.fill(color)
        self.rect: pygame.Rect = self.surface.get_rect(center=position)
        self.text: pygame.Surface = font.render(text, True, font_color)
        self.text_rect: pygame.Rect = self.text.get_rect(
            center=(self.surface.get_width() / 2, self.surface.get_height() / 2))

        self.function: Callable[[], typing.Any] = function
        self.active: Callable[[], bool] = active

    def draw(self, screen: pygame.Surface) -> None:
        self.surface.blit(self.text, self.text_rect)
        screen.blit(self.surface, self.rect)

    def click(self) -> typing.Any:
        if self.active():
            return self.function()


class Image:
    def __init__(self, path: str, position: tuple[int, int], size: tuple[int, int] | None = None) -> None:
        self.surface: pygame.Surface = pygame.image.load(path).convert_alpha()
        if size:
            self.surface = pygame.transform.scale(self.surface, size)
        self.rect: pygame.Rect = self.surface.get_rect(center=position)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)


class Text:
    def __init__(self, text: str, position: tuple[int, int], font: pygame.font.Font,
                 color: tuple[int, int, int] | str) -> None:
        self.surface: pygame.Surface = font.render(text, True, color)
        self.rect: pygame.Rect = self.surface.get_rect(center=position)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)


class UpgradeCard:
    def __init__(self, position: tuple[int, int], size: tuple[int, int], text: str, font: pygame.font.Font, image: str,
                 color: tuple[int, int, int] | str, font_color: tuple[int, int, int] | str, function: Callable[[], typing.Any]) -> None:
        self.surface: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
        self.image: Image = Image(image, position)
        self.name: Text = Text(text, (position[0], position[1] + 100), font, font_color)
        self.button: Button = Button((100, 50), (position[0], position[1] + 200),
                                     "Buy", font, color, font_color, function)

    def draw(self, screen: pygame.Surface) -> None:
        self.image.draw(screen)
        self.name.draw(screen)
        self.button.draw(screen)
