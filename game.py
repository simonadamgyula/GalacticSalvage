import pygame
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

    def run(self) -> None:
        bg_surf = self.background_generate()
        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
            self.player.rotate(keys[pygame.K_LEFT] - keys[pygame.K_RIGHT])

            self.player.update(self.screen, keys[pygame.K_UP])

            self.screen.blit(bg_surf, (0, 0))
            self.player.draw(self.screen)

            pygame.display.update()

            self.clock.tick(60)

        pygame.quit()

    def background_generate(self):
        bg_surf = pygame.image.load("img/background/space.png").convert_alpha()
        return bg_surf
