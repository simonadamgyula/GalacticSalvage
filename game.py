from enum import Enum
from collections.abc import Callable

import pygame

from meteorite import Meteorite
from player import Player
from debris import Debris
from upgrade import UpgradeManager

from uielemnts import Button, UpgradeCard

GameState = Enum("GameState", ["MAIN_MENU", "IN_GAME", "UPGRADE_MENU"])


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
        self.game_state: GameState = GameState["MAIN_MENU"]
        self.game_font = pygame.font.Font("font/Beyonders-6YoJM.ttf", 80)
        self.game_font_smaller = pygame.font.Font("font/Beyonders-6YoJM.ttf", 40)
        self.upgrade_button_font: pygame.font.Font = pygame.font.Font("font/Beyonders-6YoJM.ttf", 20)
        self.other_font = pygame.font.Font("font/ninifont-caps.otf", 50)

        self.meteorite_spawn_rate: float = 0.5  # hány darab keletkezzen másodpercenként
        self.meteor_spawn_event: int = pygame.event.custom_type()
        Meteorite.create_random(self.screen_resolution)

        self.debris_spawn_rate: float = 0.2
        self.debris_spawn_event: int = pygame.event.custom_type()
        Debris.create_random(self.screen_resolution)

        self.points: int = 0
        self.point_multiplier: int = 10

        self.upgrade_manager: UpgradeManager = UpgradeManager({
            # "max_velocity": 4,
            # "acceleration": 2,
            # "grabber_speed": 2,w
            # "rotation_speed": 2,
            # "can_slow_down": 1,
        })
        self.player.load_upgrades(self.upgrade_manager.get_upgrade_values)

        self.upgrade_button: Button = Button((200, 100), (800, 750), "Upgrade", self.upgrade_button_font,
                                             (63, 63, 63), "white",
                                             lambda: self.set_game_state(GameState["UPGRADE_MENU"]),
                                             lambda: self.game_state == GameState["MAIN_MENU"])
        self.back_button: Button = Button((100, 100), (100, 100), "Back", self.upgrade_button_font,
                                          (63, 63, 63), "white", lambda: self.set_game_state(GameState["MAIN_MENU"]),
                                          lambda: self.game_state == GameState["UPGRADE_MENU"])

        self.upgrade_cards: list[UpgradeCard] = []
        self.new_upgrades()

    def run(self) -> None:
        # main menu
        bg_surf: pygame.Surface = self.background_generate()
        title_surf: pygame.Surface = self.game_font.render(
            "Galactic Salvage", True, "white"
        )
        title_rect: pygame.Rect = title_surf.get_rect(center=(800, 330))
        run_surf: pygame.Surface = self.game_font_smaller.render(
            "Nyomd meg a szóközt az indításhoz!", True, "white"
        )
        run_rect: pygame.Rect = run_surf.get_rect(center=(800, 470))

        button_surf: pygame.Surface = pygame.Surface((100, 100))
        # button_surf.fill("black")
        button_rect: pygame.Rect = pygame.Rect(50, 50, 100, 100)
        button_text: pygame.Surface = self.game_font_smaller.render("?", True, "white")
        button_text_rect: pygame.Rect = button_text.get_rect(
            center=(button_surf.get_width() / 2, button_surf.get_height() / 2))
        screen_note: bool = False

        # in game
        pygame.time.set_timer(self.meteor_spawn_event, int(1000 / self.meteorite_spawn_rate))
        pygame.time.set_timer(self.debris_spawn_event, int(1000 / self.debris_spawn_rate))
        font_color: tuple[int, int, int] = (255, 87, 51)
        game_font = pygame.font.Font(None, 200)
        text_surf = game_font.render('DEFEAT', True, font_color)
        text_rect = text_surf.get_rect(center=(1600 / 2, 900 / 2))

        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.player.grabber.extend()
                    if button_rect.collidepoint(pygame.mouse.get_pos()) and self.game_state == GameState["MAIN_MENU"]:
                        screen_note = not screen_note
                    else:
                        pygame.draw.rect(button_surf, (0, 0, 0), (0, 0, 200, 200))

                    if self.upgrade_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.upgrade_button.click()
                    if self.back_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.back_button.click()

                    for card in self.upgrade_cards:
                        if card.button.rect.collidepoint(pygame.mouse.get_pos()):
                            success: bool = card.button.click()
                            print(success)
                if self.game_state == GameState["IN_GAME"]:
                    if event.type == self.meteor_spawn_event:
                        Meteorite.create_random(self.screen_resolution)
                    if event.type == self.debris_spawn_event:
                        Debris.create_random(self.screen_resolution)

            keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
            if self.game_state == GameState["IN_GAME"]:
                self.player.rotate((keys[pygame.K_LEFT] or keys[pygame.K_a]) -
                                   (keys[pygame.K_RIGHT] or keys[pygame.K_d]))

                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.player.accelerate()
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.player.slow_down()

                self.screen.blit(bg_surf, (0, 0))
                text_points = game_font.render(f"{self.points}", 1, font_color)
                self.screen.blit(text_points, (20, 20))
                Meteorite.meteorites.update(screen=self.screen)  # type: ignore
                Debris.debris_group.update(screen=self.screen)  # type: ignore

                if self.player.dead:
                    self.screen.blit(text_surf, text_rect)

                self.points += self.player.update() * self.point_multiplier
                self.player.grabber.check_collect(Debris.debris_group.sprites())  # type: ignore
                collision: bool = self.player.check_collision(Meteorite.meteorites.sprites())  # type: ignore
                if collision:
                    self.player.die()
                self.player.draw(self.screen)

            elif self.game_state == GameState["MAIN_MENU"]:
                self.screen.fill("black")
                if keys[pygame.K_SPACE]:
                    self.game_state = GameState["IN_GAME"]

                button_surf.blit(button_text, button_text_rect)
                self.screen.blit(button_surf, button_rect)

                if screen_note:
                    pygame.draw.rect(self.screen, "white", (300, 200, 1000, 500), border_radius=50)
                else:
                    self.screen.blit(title_surf, title_rect)
                    self.screen.blit(run_surf, run_rect)
                    self.upgrade_button.draw(self.screen)
            elif self.game_state == GameState["UPGRADE_MENU"]:
                self.screen.fill("blue")
                self.back_button.draw(self.screen)
                self.draw_upgrade_cards()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    def set_game_state(self, state: GameState) -> None:
        self.game_state = state

    def draw_upgrade_cards(self) -> None:
        for card in self.upgrade_cards:
            card.draw(self.screen)

    def new_upgrades(self) -> None:
        rand_upgrades: list[tuple[str, int, int]] = self.upgrade_manager.get_random_upgrades(3)
        self.upgrade_cards = []

        for index, upgrade in enumerate(rand_upgrades):
            self.upgrade_cards.append(UpgradeCard((400 * (index + 1), 400), (200, 300),
                                                  upgrade[0], self.upgrade_button_font, "img/debris/satellite.png",
                                                  "black", "white",
                                                  self.upgrade_card_click(upgrade[0])))

    # don't know why this is needed, but doesn't work without it
    def upgrade_card_click(self, upgrade_name: str) -> Callable[[], bool]:
        return lambda: self.upgrade_manager.try_buy(upgrade_name, self.points)

    @staticmethod
    def background_generate():
        bg_surf = pygame.image.load("img/background/space.png").convert_alpha()
        return bg_surf
