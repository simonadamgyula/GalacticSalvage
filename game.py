import json
import typing
from collections.abc import Callable
from enum import Enum

import pygame

from debris import Debris
from laser import Laser
from meteorite import Meteorite
from player import Player
from uielemnts import Button, Counter, UpgradeCard
from upgrade import UpgradeManager

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

        self.counter_font: pygame.font.Font = pygame.font.Font(None, 200)
        self.game_font: pygame.font.Font = pygame.font.Font(
            "font/Beyonders-6YoJM.ttf", 80
        )
        self.game_font_smaller: pygame.font.Font = pygame.font.Font(
            "font/Beyonders-6YoJM.ttf", 40
        )
        self.score_font: pygame.font.Font = pygame.font.Font(
            "font/Beyonders-6YoJM.ttf", 30
        )
        self.upgrade_button_font: pygame.font.Font = pygame.font.Font(
            "font/Beyonders-6YoJM.ttf", 20
        )
        self.other_font = pygame.font.Font("font/ninifont-caps.otf", 50)
        self.font_color = pygame.Color(255, 87, 51)

        self.meteorite_spawn_rate: float = 0.5  # hány darab keletkezzen másodpercenként
        self.meteor_spawn_event: int = pygame.event.custom_type()
        Meteorite.create_random(self.screen_resolution)

        self.debris_spawn_rate: float = 0.2
        self.debris_spawn_event: int = pygame.event.custom_type()
        Debris.create_random(self.screen_resolution)
        # Lézerrel kapcsolatos dolgok
        self.laser: Laser = Laser(
            (
                self.screen_resolution[0] - 50,
                self.screen_resolution[1] + self.screen_resolution[1],
            ),
            self.screen,
        )
        self.laser_spawn: int = pygame.event.custom_type()
        self.laser_timer: int = pygame.event.custom_type()
        self.warning_spawn: int = pygame.event.custom_type()
        self.warning_timer: int = pygame.event.custom_type()
        self.laser_back: int = pygame.event.custom_type()
        self.can_count_laser: bool = True
        # ----------------------------------------------------
        self.current_points: int = 0
        self.points: int = 145
        self.point_multiplier: int = 10

        self.upgrade_manager: UpgradeManager = UpgradeManager({})

        self.player.load_upgrades(self.upgrade_manager.get_upgrade_values)

        self.screen_note: bool = False
        self.help_button: Button = Button(
            (100, 100),
            "?",
            self.game_font_smaller,
            None,
            "white",
            lambda: self.toggle_screen_note(),
            lambda: self.game_state == GameState["MAIN_MENU"],
            center=(100, 100),
        )

        self.upgrade_button: Button = Button(
            (200, 100),
            "upgrade",
            self.upgrade_button_font,
            (63, 63, 63),
            "white",
            lambda: self.set_game_state(GameState["UPGRADE_MENU"]),
            lambda: self.game_state == GameState["MAIN_MENU"],
            center=(800, 750),
        )
        self.back_button: Button = Button(
            (100, 100),
            "back",
            self.upgrade_button_font,
            (63, 63, 63),
            "white",
            lambda: self.set_game_state(GameState["MAIN_MENU"]),
            lambda: self.game_state == GameState["UPGRADE_MENU"],
            center=(100, 100),
        )
        self.laser_button: Button = Button(
            (500, 100),
            "lézer",
            self.score_font,
            (0, 0, 0),
            "white",
            lambda: self.toggle_laser(),
            lambda: self.game_state == GameState["MAIN_MENU"],
            center=(1400, 50),
        )
        self.point_counter: Counter = Counter(
            self.game_font_smaller, "", (255, 255, 255), center=(300, 100)
        )
        self.in_game_counter: Counter = Counter(
            self.score_font, "Jelenlegi pontszámod: ", (255, 255, 255), topleft=(20, 20)
        )

        self.upgrade_cards: list[UpgradeCard] = []
        self.new_upgrades()

        self.load()

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

        pygame.time.set_timer(
            self.meteor_spawn_event, int(1000 / self.meteorite_spawn_rate)
        )
        pygame.time.set_timer(
            self.debris_spawn_event, int(1000 / self.debris_spawn_rate)
        )
        pygame.time.set_timer(self.warning_spawn, int(9000))  # első lézer 9sec

        text_surf: pygame.Surface = self.game_font.render(
            "Meghaltál!", True, self.font_color
        )
        text_rect: pygame.Rect = text_surf.get_rect(center=(1600 / 2, 900 / 2))

        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.player.grabber.extend()
                    Button.handle_clicks()

                if self.game_state == GameState["IN_GAME"]:
                    if event.type == self.meteor_spawn_event:
                        Meteorite.create_random(self.screen_resolution)
                    if event.type == self.debris_spawn_event:
                        Debris.create_random(self.screen_resolution)

                if self.laser.enabled:
                    if self.laser.all_laser >= 10:
                        self.laser.two_laser = True
                    if event.type == self.warning_spawn:
                        self.laser.get_pos()
                        self.laser.show_warning = True
                        pygame.time.set_timer(self.warning_timer, int(2000), 1)
                    if event.type == self.warning_timer:
                        self.laser.show_warning = False
                        self.laser.laser_go = True
                        pygame.time.set_timer(self.laser_timer, int(700), 1)
                    if event.type == self.laser_timer:
                        self.laser.laser_go = False
                        self.laser.all_laser += 1
                # ------------------------------------------------
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_state == GameState["MAIN_MENU"]:
                            self.set_game_state(GameState["IN_GAME"])
                        elif (
                                self.game_state == GameState["IN_GAME"] and self.player.dead
                        ):
                            self.reset()

            keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
            if self.game_state == GameState["IN_GAME"]:
                self.player.rotate(
                    (keys[pygame.K_LEFT] or keys[pygame.K_a])
                    - (keys[pygame.K_RIGHT] or keys[pygame.K_d])
                )

                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.player.accelerate()
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.player.slow_down()

                self.screen.blit(bg_surf, (0, 0))

                self.in_game_counter.update(self.current_points)
                self.in_game_counter.draw(self.screen)

                Meteorite.meteorites.update(screen=self.screen)  # type: ignore
                Debris.debris_group.update(screen=self.screen)  # type: ignore

                if self.player.dead:
                    self.screen.blit(text_surf, text_rect)

                self.current_points += self.player.update() * self.point_multiplier
                self.player.grabber.check_collect(Debris.debris_group.sprites())  # type: ignore
                collision: bool = self.player.check_collision(Meteorite.meteorites.sprites())  # type: ignore

                if collision:
                    self.player.get_hit()
                self.player.draw(self.screen)

                if (
                        self.player.check_kill_collision(
                            self.laser.kill_rect,
                            self.laser.kill_rect_ver,
                            self.laser.direction,
                        )
                        and self.laser.laser_go
                ):
                    self.player.die()

                self.laser.update(self.screen)
            elif self.game_state == GameState["MAIN_MENU"]:
                self.screen.fill("black")
                self.help_button.draw(self.screen)

                if self.screen_note:
                    pygame.draw.rect(
                        self.screen, "white", (300, 200, 1000, 500), border_radius=50
                    )
                else:
                    self.screen.blit(title_surf, title_rect)
                    self.screen.blit(run_surf, run_rect)

                    self.upgrade_button.draw(self.screen)
                    self.laser_button.draw(self.screen)
            elif self.game_state == GameState["UPGRADE_MENU"]:
                self.screen.fill("blue")

                self.point_counter.update(self.points)
                self.point_counter.draw(self.screen)

                self.back_button.draw(self.screen)
                self.draw_upgrade_cards()

            pygame.display.update()
            self.clock.tick(60)

        self.save()
        pygame.quit()

    def reset(self) -> None:
        self.player.reset()
        self.new_upgrades()
        self.set_game_state(GameState["MAIN_MENU"])
        Meteorite.meteorites.empty()
        Debris.debris_group.empty()

        self.points += self.current_points
        self.current_points = 0

        self.laser.all_laser = 0
        pygame.time.set_timer(self.warning_spawn, 0)
        pygame.time.set_timer(self.warning_spawn, int(9000))

        self.save()

    def set_game_state(self, state: GameState) -> None:
        self.game_state = state

    def toggle_screen_note(self) -> None:
        self.screen_note = not self.screen_note

    def draw_upgrade_cards(self) -> None:
        for card in self.upgrade_cards:
            card.draw(self.screen)

    def new_upgrades(self) -> None:
        rand_upgrades: list[tuple[str, int, int]] = (
            self.upgrade_manager.get_random_upgrades(3)
        )
        self.upgrade_cards = []

        for index, upgrade in enumerate(rand_upgrades):
            callables: tuple[Callable[[], typing.Any], Callable[[], bool]] = (
                self.create_callables(upgrade[0])
            )
            self.upgrade_cards.append(
                UpgradeCard(
                    (200, 300),
                    upgrade[0],
                    upgrade[2],
                    self.upgrade_button_font,
                    "img/debris/satellite.png",
                    "black",
                    "white",
                    callables[0],
                    callables[1],
                    center=(400 * (index + 1), 400),
                )
            )

    # don't know why this is needed, but doesn't work without it
    def create_callables(
            self, upgrade_name: str
    ) -> tuple[Callable[[], typing.Any], Callable[[], bool]]:
        return (
            lambda: self.try_buy(upgrade_name),
            lambda: self.upgrade_manager.can_buy(upgrade_name, self.points),
        )

    def try_buy(self, upgrade_name: str) -> None:
        cost: int = self.upgrade_manager.try_buy(upgrade_name, self.points)
        self.points -= cost
        self.save()
        self.player.load_upgrades(self.upgrade_manager.get_upgrade_values)

    @staticmethod
    def background_generate():
        bg_surf = pygame.image.load("img/background/space.png").convert_alpha()
        return bg_surf

    def toggle_laser(self):
        self.laser.enabled = not self.laser.enabled
        if self.laser.enabled:
            self.laser_button.bg_color = (70, 150, 110)
        else:
            self.laser_button.bg_color = (0, 0, 0)

    def save(self) -> None:
        save_dict: dict[str, int | dict[str, int]] = {
            "points": self.points,
            "upgrades": self.upgrade_manager.upgrades
        }
        with open("saves.json", "w", encoding="utf-8") as file:
            json.dump(save_dict, file)

    def load(self) -> None:
        try:
            with open("saves.json", "r", encoding="utf-8") as file:
                load_dict = json.load(file)
        except FileNotFoundError:
            return

        self.points = load_dict.get("points", 0)
        self.upgrade_manager = UpgradeManager(load_dict.get("upgrades", {}))
        self.player.load_upgrades(self.upgrade_manager.get_upgrade_values)
