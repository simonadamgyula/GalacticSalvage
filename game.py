from pydoc import plain
import pygame

from meteorite import Meteorite
from player import Player


class Game:

    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_caption("Galactic Salvage")
        self.screen_resolution: tuple[int, int] = (1600, 900)

        self.screen: pygame.Surface = pygame.display.set_mode(self.screen_resolution)
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.player: Player = Player(
            self.screen_resolution[0] // 2, self.screen_resolution[1] // 2, 0
        )

        self.meteorite_spawn_rate: float = 0.5  # hány darab keletkezzen másodpercenként
        self.meteor_event: int = pygame.event.custom_type()
        Meteorite.create_random(self.screen_resolution)

    def run(self) -> None:
        bg_surf = self.background_generate()
        running: bool = True

        pygame.time.set_timer(self.meteor_event, int(1000 / self.meteorite_spawn_rate))
        Font_color = (255,87,51)
        game_font = pygame.font.Font(None, 200)
        text_surf = game_font.render('DEFEAT', True, Font_color)
        text_rect = text_surf.get_rect(center=(1600 / 2, 900 / 2))

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self.player.grabber.extend()
                if event.type == self.meteor_event:
                    Meteorite.create_random(self.screen_resolution)

            keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
            self.player.rotate((keys[pygame.K_LEFT] or keys[pygame.K_a]) - (keys[pygame.K_RIGHT] or keys[pygame.K_d]))

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.accelerate()
            pygame.display.update()

            self.screen.blit(bg_surf, (0, 0))

            Meteorite.meteorites.update(screen=self.screen)
            self.player.draw(self.screen)
            if self.player.dying:
                self.screen.blit(text_surf, text_rect)

            self.player.update()
            collision: bool = self.player.check_collision(Meteorite.meteorites.sprites())
            self.player.draw(self.screen, collision)

            self.clock.tick(60)

        pygame.quit()

    @staticmethod
    def background_generate():
        bg_surf = pygame.image.load("img/background/space.png").convert_alpha()
        return bg_surf
