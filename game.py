import pygame

from debris import Debris
from laser import Laser
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
        self.game_active: bool = False
        self.game_font = pygame.font.Font("font/Beyonders-6YoJM.ttf", 80)
        self.game_font_smaller = pygame.font.Font("font/Beyonders-6YoJM.ttf", 40)
        self.other_font = pygame.font.Font("font/ninifont-caps.otf", 50)

        self.meteorite_spawn_rate: float = 0.5  # hány darab keletkezzen másodpercenként
        self.meteor_spawn_event: int = pygame.event.custom_type()
        Meteorite.create_random(self.screen_resolution)

        self.debris_spawn_rate: float = 0.2
        self.debris_spawn_event: int = pygame.event.custom_type()
        Debris.create_random(self.screen_resolution)
        self.laser = Laser(
            (
                self.screen_resolution[0] - 50,
                self.screen_resolution[1] + self.screen_resolution[1],
            ),
            self.screen,
        )

        self.warning_clock = 0

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
        # button_surf.fill("black")
        button_rect: pygame.Rect = pygame.Rect(50, 50, 100, 100)
        button_text: pygame.Surface = self.game_font_smaller.render("?", True, "white")
        button_text_rect: pygame.Rect = button_text.get_rect(
            center=(button_surf.get_width() / 2, button_surf.get_height() / 2)
        )
        screen_note: bool = False

        running: bool = True

        pygame.time.set_timer(
            self.meteor_spawn_event, int(1000 / self.meteorite_spawn_rate)
        )
        pygame.time.set_timer(
            self.debris_spawn_event, int(1000 / self.debris_spawn_rate)
        )
        Font_color = (255, 87, 51)
        game_font = pygame.font.Font(None, 200)
        text_surf = game_font.render("DEFEAT", True, Font_color)
        text_rect = text_surf.get_rect(center=(1600 / 2, 900 / 2))

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.player.grabber.extend()
                    if button_rect.collidepoint(pygame.mouse.get_pos()):
                        screen_note = not screen_note

                    else:
                        pygame.draw.rect(button_surf, (0, 0, 0), (0, 0, 200, 200))
                if event.type == self.meteor_spawn_event:
                    Meteorite.create_random(self.screen_resolution)
                if event.type == self.debris_spawn_event:
                    Debris.create_random(self.screen_resolution)
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if pygame.mouse.get_pressed()[0]:
                #         self.player.grabber.extend()

            keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
            if self.game_active:
                self.player.rotate(
                    (keys[pygame.K_LEFT] or keys[pygame.K_a])
                    - (keys[pygame.K_RIGHT] or keys[pygame.K_d])
                )

                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.player.accelerate()

                self.screen.blit(bg_surf, (0, 0))
                text_points = game_font.render(
                    f"{self.player.grabber.points}", 1, Font_color
                )
                self.screen.blit(text_points, (20, 20))
                Meteorite.meteorites.update(screen=self.screen)
                Debris.debris_group.update(screen=self.screen)

                if self.player.dead:
                    self.screen.blit(text_surf, text_rect)

                self.player.update()
                self.player.grabber.check_collect(
                    Debris.debris_group.sprites(), screen=self.screen
                )
                collision: bool = self.player.check_collision(
                    Meteorite.meteorites.sprites()
                ) 
                if collision:
                    self.player.die()
                self.player.draw(self.screen)

                if self.player.check_kill_collision(self.laser.kill_rect) and self.laser.laser_go:
                    self.player.die()

                self.warning_clock += 1
                if self.warning_clock % 300 == 0:
                    self.laser.get_pos()
                    self.laser.show_warning = True

                if self.laser.show_warning:

                    self.laser.warning_timer += 1
                    if self.laser.warning_timer >= 120:
                        self.laser.show_warning = False
                        self.laser.laser_go = True
                        self.laser.warning_timer = 0

                if self.laser.laser_go:

                    self.laser.laser_go_timer += 1
                    if self.laser.laser_go_timer >= 120:
                        self.laser.laser_go = False
                        self.warning_clock = 0
                        self.laser.laser_go_timer = 0
                

                self.laser.update(self.screen)
            else:
                self.screen.fill("green")
                if keys[pygame.K_SPACE]:
                    self.game_active = True

                button_surf.blit(button_text, button_text_rect)
                self.screen.blit(button_surf, button_rect)
                if screen_note:
                    pygame.draw.rect(
                        self.screen, "white", (300, 200, 1000, 500), border_radius=50
                    )
                else:
                    self.screen.blit(title_surf, title_rect)
                    self.screen.blit(run_surf, run_rect)

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    @staticmethod
    def background_generate():
        bg_surf = pygame.image.load("img/background/space.png").convert_alpha()
        return bg_surf
