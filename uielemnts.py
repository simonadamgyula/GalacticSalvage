import typing

from collections.abc import Callable
import pygame

from sound import Sound


class Button:
    buttons: list["Button"] = []

    def __init__(
        self,
        size: tuple[int, int],
        text: str,
        font: pygame.font.Font,
        bg_color: tuple[int, int, int] | str | None,
        font_color: tuple[int, int, int] | str,
        function: Callable[[], typing.Any],
        active: Callable[[], bool] = lambda: True,
        usage: int = -1,
        disabled_color: tuple[int, int, int] | str = "gray",
        **position: tuple[int, int],
    ) -> None:
        self.surface: pygame.Surface = pygame.Surface(
            size, pygame.SRCALPHA, 32
        ).convert_alpha()
        self.rect: pygame.Rect = self.surface.get_rect(**position)
        self.text: pygame.Surface = font.render(text, True, font_color)
        self.text_rect: pygame.Rect = self.text.get_rect(
            center=(self.surface.get_width() / 2, self.surface.get_height() / 2)
        )

        self.bg_color: tuple[int, int, int] | str | None = bg_color
        self.disabled_color: tuple[int, int, int] | str = disabled_color

        self.usage: int = usage

        self.function: Callable[[], typing.Any] = function
        self.active: Callable[[], bool] = active

        Button.buttons.append(self)

        self.sound = Sound()

    def draw(self, screen: pygame.Surface) -> None:
        if self.bg_color is not None:
            self.surface.fill(
                self.bg_color
                if (self.usage != 0 and self.active())
                else self.disabled_color
            )
        self.surface.blit(self.text, self.text_rect)
        screen.blit(self.surface, self.rect)

    def click(self) -> typing.Any:
        if self.usage == 0:
            self.sound.wrong_button.play()
            return
        self.usage -= 1 if self.usage > 0 else 0

        if self.active():
            self.sound.button.play()
            return self.function()

    @staticmethod
    def handle_clicks() -> None:
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        for button in Button.buttons:
            if button.rect.collidepoint(mouse_pos):
                button.click()


class Image:
    def __init__(
        self,
        path: str,
        size: tuple[int, int] | float | None = None,
        **position: tuple[int, int],
    ) -> None:
        self.surface: pygame.Surface = pygame.image.load(path).convert_alpha()
        if size:
            if isinstance(size, tuple):
                self.surface = pygame.transform.scale(self.surface, size)
            elif isinstance(size, float):
                self.surface = pygame.transform.scale_by(self.surface, (size, size))
        self.rect: pygame.Rect = self.surface.get_rect(**position)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)


class Text:
    def __init__(self, text: str, font: pygame.font.Font, color: tuple[int, int, int] | str,
                 line_height: int = 30, **position: tuple[int, int]) -> None:
        lines: list[str] = text.split("\n")
        self.surfaces: list[pygame.Surface] = []
        self.line_height: int = line_height

        self.position: dict[str, tuple[int, int]] = position
        self.position_anchor: str = list(self.position.keys())[0]

        for line in lines:
            self.surfaces.append(font.render(line, True, color))

    def draw(self, screen: pygame.Surface) -> None:
        for index, surface in enumerate(self.surfaces):
            position: tuple[int, int] = self.position[self.position_anchor]
            position = (position[0], position[1] + (self.line_height * index))
            rect = surface.get_rect(**{self.position_anchor: position})
            screen.blit(surface, rect)


class Counter:
    def __init__(
        self,
        font: pygame.font.Font,
        text: str,
        color: tuple[int, int, int] | str,
        **position: tuple[int, int],
    ) -> None:
        self.count: float = 0

        self.text = text
        self.font: pygame.font.Font = font
        self.color: tuple[int, int, int] | str = color
        self.position: dict[str, tuple[int, int]] = position

        self.surface: pygame.Surface = font.render(str(self.count), True, color)
        self.rect: pygame.Rect = self.surface.get_rect(**position)

    def update(self, count: float) -> None:
        self.count = count
        self.surface = self.font.render(self.text + str(self.count), True, self.color)
        self.rect = self.surface.get_rect(**self.position)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)


class UpgradeCard:
    def __init__(self, size: tuple[int, int], text: str, price: int, font: pygame.font.Font,
                 image: str, color: tuple[int, int, int] | str, font_color: tuple[int, int, int] | str,
                 function: Callable[[], typing.Any], active: Callable[[], bool], description: str,
                 description_font: pygame.font.Font, disabled_color: tuple[int, int, int] | str = "gray",
                 **position: tuple[int, int]) -> None:
        self.surface: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()

        position: tuple[int, int] = position.get("center", (0, 0))

        self.image: Image = Image(image, float(2), center=position)
        self.name: Text = Text(text, font, font_color, center=(position[0], position[1] + 100))
        self.price_text: Text = Text(f"Price: {price}", font, font_color, center=(position[0], position[1] + 200))
        self.description: Text = Text(description, description_font, "white", center=(position[0], position[1] + 270))
        self.button: Button = Button((100, 50),
                                     "Buy", font, color, font_color, function, active=active,
                                     usage=1, disabled_color=disabled_color, center=(position[0], position[1] + 400))

    def draw(self, screen: pygame.Surface) -> None:
        self.image.draw(screen)
        self.name.draw(screen)
        self.price_text.draw(screen)
        self.description.draw(screen)
        self.button.draw(screen)
