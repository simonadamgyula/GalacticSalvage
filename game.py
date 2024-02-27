import pygame
from player import Player


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen_resolution: tuple[int, int] = (1000, 800)

        self.screen: pygame.Surface = pygame.display.set_mode(self.screen_resolution)
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.player: Player = Player(self.screen_resolution[0] // 2, self.screen_resolution[1] // 2, 0)

    def run(self) -> None:
        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
            self.player.rotate(keys[pygame.K_LEFT] - keys[pygame.K_RIGHT])

            self.screen.fill((0, 0, 0))

            self.player.update(self.screen)

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.accelerate()
            pygame.display.update()

            self.clock.tick(60)

        pygame.quit()
