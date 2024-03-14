import typing

from collections.abc import Callable
import pygame


def log(*, center: typing.Any) -> None:
    print(center)


class Button:
    def __init__(self, size: tuple[int, int], text: str, font: pygame.font.Font, bg_color: tuple[int, int, int] | str,
                 font_color: tuple[int, int, int] | str, function: Callable[[], typing.Any],
                 active: Callable[[], bool] = lambda: True, usage: int = -1,
                 disabled_color: tuple[int, int, int] | str = "gray", **position: tuple[int, int]) -> None:
        self.surface: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
        log(**position)
        self.rect: pygame.Rect = self.surface.get_rect(**position)
        self.text: pygame.Surface = font.render(text, True, font_color)
        self.text_rect: pygame.Rect = self.text.get_rect(
            center=(self.surface.get_width() / 2, self.surface.get_height() / 2))

        self.bg_color: tuple[int, int, int] | str = bg_color
        self.disabled_color: tuple[int, int, int] | str = disabled_color

        self.usage: int = usage

        self.function: Callable[[], typing.Any] = function
        self.active: Callable[[], bool] = active

    def draw(self, screen: pygame.Surface) -> None:
        self.surface.fill(self.bg_color if (self.usage != 0 and self.active()) else self.disabled_color)
        self.surface.blit(self.text, self.text_rect)
        screen.blit(self.surface, self.rect)

    def click(self) -> typing.Any:
        if self.usage == 0:
            return
        self.usage -= 1 if self.usage > 0 else 0

        if self.active():
            return self.function()


class Image:
    def __init__(self, path: str, size: tuple[int, int] | None = None, **position: tuple[int, int]) -> None:
        self.surface: pygame.Surface = pygame.image.load(path).convert_alpha()
        if size:
            self.surface = pygame.transform.scale(self.surface, size)
        self.rect: pygame.Rect = self.surface.get_rect(**position)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)


class Text:
    def __init__(self, text: str, font: pygame.font.Font,
                 color: tuple[int, int, int] | str, **position: tuple[int, int]) -> None:
        self.surface: pygame.Surface = font.render(text, True, color)
        self.rect: pygame.Rect = self.surface.get_rect(**position)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)


class Counter:
    def __init__(self, font: pygame.font.Font,
                 color: tuple[int, int, int] | str, **position: tuple[int, int]) -> None:
        self.count: float = 0

        self.font: pygame.font.Font = font
        self.color: tuple[int, int, int] | str = color
        self.position: dict[str, tuple[int, int]] = position

        self.surface: pygame.Surface = font.render(str(self.count), True, color)
        self.rect: pygame.Rect = self.surface.get_rect(**position)

    def update(self, count: float) -> None:
        self.count = count
        self.surface = self.font.render(str(self.count), True, self.color)
        self.rect = self.surface.get_rect(**self.position)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)


class UpgradeCard:
    def __init__(self, size: tuple[int, int], text: str, price: int, font: pygame.font.Font,
                 image: str, color: tuple[int, int, int] | str, font_color: tuple[int, int, int] | str,
                 function: Callable[[], typing.Any], active: Callable[[], bool],
                 disabled_color: tuple[int, int, int] | str = "gray", **position: tuple[int, int]) -> None:
        self.surface: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()

        position: tuple[int, int] = position.get("center", (0, 0))

        self.image: Image = Image(image, center=position)
        self.name: Text = Text(text, font, font_color, center=(position[0], position[1] + 100))
        self.price_text: Text = Text(f"Price: {price}", font, font_color, center=(position[0], position[1] + 200))
        self.button: Button = Button((100, 50),
                                     "Buy", font, color, font_color, function, active=active,
                                     usage=1, disabled_color=disabled_color, center=(position[0], position[1] + 300))

    def draw(self, screen: pygame.Surface) -> None:
        self.image.draw(screen)
        self.name.draw(screen)
        self.price_text.draw(screen)
        self.button.draw(screen)
