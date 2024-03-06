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
        self.game_active: bool = False
        self.game_font = pygame.font.Font("font/Beyonders-6YoJM.ttf", 80)
        self.game_font_smaller = pygame.font.Font("font/Beyonders-6YoJM.ttf", 40)
        self.other_font = pygame.font.Font("font/ninifont-caps.otf", 50)

    def run(self) -> None:
        bg_surf: pygame.Surface = self.background_generate()
        title_surf: pygame.Surface = self.game_font.render(
            "Galactic Salvage", True, "white"
        )
        title_rect: pygame.Rect = title_surf.get_rect(center=(800, 330))
        run_surf: pygame.Surface = self.game_font_smaller.render(
            "Nyomd meg a szóközt az indításhoz!", True, "white"
        )
        run_rect: pygame.Rect = run_surf.get_rect(center=(800, 470))

        # button properties
        button_surf: pygame.Surface = pygame.Surface((100, 100))
        button_surf.fill("white")
        button_rect: pygame.Rect = pygame.Rect(50, 50, 50, 50)
        button_text: pygame.Surface = self.game_font_smaller.render("?", True, "red", "white")
        button_text_rect: pygame.Rect = button_text.get_rect(center=(button_surf.get_width()/2, button_surf.get_height()/2))

        #how to play properties
        htp_surf: pygame.Surface = pygame.Surface((400, 400))
        htp_surf.fill("blue")
        htp_rect: pygame.Rect = pygame.Rect(200, 200, 200, 200)
        htp_text: pygame.Surface = self.other_font.render("How to play", True, "green")
        htp_text_surf: pygame.Rect = htp_rect.get_rect(center=(button_surf.get_width()/2, button_surf.get_height()/2))

        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(button_surf, "blue", (200, 200))
                    else:
                        pygame.draw.rect(button_surf, (255, 255, 255), (0, 0, 200, 200))
                        pygame.draw.rect(button_surf, (255, 255, 255), (1, 1, 148, 48))
                        pygame.draw.rect(button_surf, (0, 0, 0), (1, 1, 148, 1), 2)
                        pygame.draw.rect(button_surf, (0, 100, 0), (1, 48, 148, 10), 2)
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if pygame.mouse.get_pressed()[0]:
                #         self.player.grabber.extend()

            keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
            if self.game_active:
                self.player.rotate(
                    (keys[pygame.K_LEFT] or keys[pygame.K_a])
                    - (keys[pygame.K_RIGHT] or keys[pygame.K_d])
                )

                self.screen.blit(bg_surf, (0, 0))
                self.player.draw(self.screen)

                self.player.update(self.screen)

                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.player.accelerate()

            else:
                self.screen.blit(title_surf, title_rect)
                self.screen.blit(run_surf, run_rect)

                if keys[pygame.K_SPACE]:
                    self.game_active = True

                

            button_surf.blit(button_text, button_text_rect)
            self.screen.blit(button_surf, button_rect)
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    def background_generate(self):
        bg_surf = pygame.image.load("img/background/space.png").convert_alpha()
        return bg_surf
