import math
from copy import copy

import pygame

from animation import Animation
from collision import Collision
from grabber import Grabber
from meteorite import Meteorite
from sound import Sound


def clamp(value: float, min_: float, max_: float) -> float:
    return max(min(value, max_), min_)


def map_value_to_range(
    value: float, start1: float, stop1: float, start2: float, stop2: float
) -> float:
    range1: float = stop1 - start1
    range2: float = stop2 - start2
    difference: float = range1 / range2

    return (value - start1) * difference + start2


class Player:
    def __init__(self, x: int, y: int, direction: float) -> None:
        self.starting_position: pygame.Vector2 = pygame.Vector2(x, y)
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.direction: float = direction

        self.rotation_speed: float = 2

        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.acceleration: float = 0.5
        self.deceleration: float = 0.02
        self.max_velocity: float = 3

        self.nmoving_anim: Animation = Animation.import_spritesheet("img/spaceship/default/not_moving.png", 72, 120,
                                                                    0.2, True)
        self.moving_anim: Animation = Animation.import_spritesheet("img/spaceship/default/moving.png", 72, 120,
                                                                   0.3, True)

        self.death_animation: Animation = Animation.import_spritesheet(
            "img/explosion.png", 224, 224, 0.2, False
        )

        self.shield_image: pygame.Surface = pygame.image.load(
            "img/spaceship/shield/shield.png"
        ).convert_alpha()
        self.shield_visibility_duration: float = 30  # in frames (60 frames per second)
        self.shield_visible: float = 0
        self.shield_break_animation: Animation = Animation.import_spritesheet(
            "img/spaceship/shield/shield_break.png", 132, 132, 0.2, False
        )

        self.image: pygame.Surface = self.nmoving_anim.next()

        self.moving = False
        self.can_slow_down: bool = False
        self.max_shield: int = 0
        self.shield: int = self.max_shield

        self.grabber: Grabber = Grabber(self.position)

        self.dead = False
        self.last_meteorite_hit: Meteorite | None = None

        self.prev_call: float = 0

        self.sound = Sound()

    @property
    def resolution(self) -> tuple[int, int]:
        return self.image.get_width(), self.image.get_height()

    def reset(self) -> None:
        self.position = self.starting_position.copy()
        self.dead = False
        self.shield = copy(self.max_shield)
        self.velocity = pygame.Vector2(0, 0)
        self.death_animation.reset()
        self.shield_break_animation.reset()
        self.shield_visible = 0

    def draw(self, screen: pygame.Surface) -> None:
        if self.dead:
            self.death_animation.draw_next(screen, self.position)
            return

        self.grabber.draw(screen)

        rotated_image: pygame.Surface = pygame.transform.rotate(
            self.image, self.direction
        )
        rotated_rect: pygame.Rect = rotated_image.get_rect(
            center=self.image.get_rect(center=self.position).center
        )

        screen.blit(rotated_image, rotated_rect)
        self.draw_shield(screen)

    def update(self) -> int:
        self.animate()
        self.move()
        self.out_screen()
        return self.grabber.update(self.position)

    def accelerate(self) -> None:
        if self.shield_visible > 0:
            return

        acceleration: pygame.Vector2 = (
            pygame.Vector2(0, 1).rotate(-self.direction) * self.acceleration
        )

        self.velocity += acceleration
        self.velocity = self.velocity.clamp_magnitude(self.max_velocity)
        self.moving = True

    def slow_down(self) -> None:
        if self.can_slow_down:
            self.velocity *= 1 - self.deceleration

    def move(self) -> None:
        if self.dead:
            return
        self.position -= self.velocity

    def rotate(self, direction: float) -> None:
        self.direction += direction * self.rotation_speed
        self.direction %= 360

    def animate(self):
        if not self.moving:
            self.image = self.nmoving_anim.next()
        else:
            self.image = self.moving_anim.next()

        self.moving = False

    def get_verticies(self) -> list[pygame.Vector2]:
        width: int = self.image.get_width()
        height: int = self.image.get_height()

        verticies: list[pygame.Vector2] = []
        for i in range(4):
            binary: str = format(i, "b").zfill(2)
            verticies.append(
                pygame.Vector2(
                    (width / 2) * (1 if binary[0] == "0" else -1),
                    (height / 2) * (1 if binary[1] == "0" else -1),
                ).rotate(-self.direction)
                + self.position
            )

        verticies[-1], verticies[-2] = verticies[-2], verticies[-1]
        return verticies

    def check_collision(self, meteorites: list[Meteorite]) -> bool:
        verticies: list[pygame.Vector2] = self.get_verticies()
        for meteorite in meteorites:
            if (
                meteorite.radius
                + math.sqrt(
                    (self.image.get_width() / 2) ** 2
                    + (self.image.get_height() / 2) ** 2
                )
                < (self.position - meteorite.position).magnitude()
            ):
                continue

            if Collision.rectangle_circle_collision(
                self.position, verticies, meteorite.position, meteorite.radius
            ):
                self.last_meteorite_hit = meteorite
                return True

        return False

    def out_screen(self) -> None:
        if (
            self.position.x > 1600
            or self.position.x < 0
            or self.position.y > 900
            or self.position.y < 0
        ):
            self.die()

    def get_hit(self) -> None:
        if self.shield_visible > 0:
            return

        if self.shield == 0:
            self.die()

        self.bounce_off_meteorite(self.last_meteorite_hit)
        self.shield -= 1
        self.show_shield()

    def die(self) -> None:
        if not self.dead:
            self.dead = True
            self.sound.play_sound(self.sound.explosion)

    def check_kill_collision(
        self, kill_rect: pygame.Rect, kill_rect_ver: pygame.Rect, direction: int
    ) -> bool:
        vertices: list[pygame.Vector2] = self.get_verticies()
        for vertex in vertices:
            if direction == 1:
                if kill_rect.collidepoint(vertex.x, vertex.y):
                    return True
            else:
                if kill_rect_ver.collidepoint(vertex.x, vertex.y):
                    return True
        return False

    def load_upgrades(self, upgrades: dict[str, float | bool]) -> None:
        self.max_velocity = upgrades["max_velocity"]
        self.rotation_speed = upgrades["rotation_speed"]
        self.grabber.extension_speed = upgrades["grabber_speed"]
        self.can_slow_down = bool(upgrades["can_slow_down"])
        self.grabber.update_length(upgrades["grabber_length"])

        if upgrades["ee"]:
            self.nmoving_anim: Animation = Animation.import_spritesheet("img/spaceship/ee/not_moving.png", 72, 120,
                                                                        0.2, True)
            self.moving_anim: Animation = Animation.import_spritesheet("img/spaceship/ee/moving.png", 72, 120,
                                                                       0.3, True)
        else:
            self.nmoving_anim: Animation = Animation.import_spritesheet("img/spaceship/default/not_moving.png", 72, 120,
                                                                        0.2, True)
            self.moving_anim: Animation = Animation.import_spritesheet("img/spaceship/default/moving.png", 72, 120,
                                                                       0.3, True)

        self.max_shield = int(upgrades["shield"])
        self.shield = copy(self.max_shield)

    def bounce_off_meteorite(self, meteorite: Meteorite) -> None:
        if self.last_meteorite_hit is None:
            return

        surface_normal: pygame.Vector2 = -(
            self.position - meteorite.position
        ).normalize()
        self.velocity = surface_normal * max(
            self.velocity.magnitude(), self.max_velocity / 2
        )
        self.position += self.velocity

    def show_shield(self) -> None:
        self.shield_visible = copy(self.shield_visibility_duration)

    def draw_shield(self, screen: pygame.Surface) -> None:
        if self.shield_visible <= 0:
            self.shield_visible = 0
            return

        if self.shield == 0:
            self.shield_break_animation.draw_next(screen, self.position)
            self.shield_visible -= 1
            return

        self.shield_image.set_alpha(
            int(
                map_value_to_range(
                    self.shield_visible, 0, 255, 0, self.shield_visibility_duration
                )
            )
        )
        shield_rect: pygame.Rect = self.shield_image.get_rect(center=self.position)
        screen.blit(self.shield_image, shield_rect)
        self.shield_visible -= 1
