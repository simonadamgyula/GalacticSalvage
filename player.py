import math
import pygame
from copy import copy

from animation import Animation
from collision import Collision
from grabber import Grabber
from meteorite import Meteorite


def clamp(value: float, min_: float, max_: float) -> float:
    return max(min(value, max_), min_)


def map_value_to_range(value: float, start1: float, stop1: float, start2: float, stop2: float) -> float:
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

        self.images_nmoving: list[pygame.Surface] = []
        self.images_nmoving.append(pygame.image.load("img/spaceship/not_moving/1.png"))
        self.images_nmoving.append(pygame.image.load("img/spaceship/not_moving/2.png"))

        self.images: list[pygame.Surface] = []
        self.images.append(pygame.image.load("img/spaceship/moving/1.png"))
        self.images.append(pygame.image.load("img/spaceship/moving/2.png"))
        self.images.append(pygame.image.load("img/spaceship/moving/3.png"))
        self.images.append(pygame.image.load("img/spaceship/moving/4.png"))
        self.images.append(pygame.image.load("img/spaceship/moving/5.png"))

        self.death_animation: Animation = Animation.import_spritesheet("img/explosion.png", 224, 224, 0.2, False)

        self.shield_image: pygame.Surface = pygame.image.load("img/spaceship/shield/shield.png").convert_alpha()
        self.shield_visibility_duration: float = 30  # in frames (60 frames per second)
        self.shield_visible: float = 0
        self.shield_break_animation: Animation = Animation.import_spritesheet("img/spaceship/shield/shield_break.png",
                                                                              132, 132, 0.2, False)

        self.frame_index = 0
        self.animation_speed: float = 0.3
        self.animation_speed_nmoving: float = 0.2

        self.image: pygame.Surface = self.images_nmoving[self.frame_index]

        self.moving = False
        self.can_slow_down: bool = False
        self.max_shield: int = 0
        self.shield: int = self.max_shield

        self.grabber: Grabber = Grabber(self.position)

        self.dead = False
        self.last_meteorite_hit: Meteorite | None = None

        self.prev_call: float = 0

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

        acceleration: pygame.Vector2 = pygame.Vector2(0, 1).rotate(-self.direction) * self.acceleration

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
            self.frame_index += self.animation_speed_nmoving
            if self.frame_index >= len(self.images_nmoving):
                self.frame_index = 0
            self.image = self.images_nmoving[int(self.frame_index)]
        else:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.images):
                self.frame_index = 0
            self.image = self.images[int(self.frame_index)]

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

            if Collision.rectangle_circle_collision(self.position, verticies, meteorite.position, meteorite.radius):
                self.last_meteorite_hit = meteorite
                return True

        return False

    def out_screen(self) -> None:
        if (
                self.position.x > 1600 or self.position.x < 0 or
                self.position.y > 900 or self.position.y < 0
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
        self.dead = True


    def check_kill_collision(self, kill_rect: pygame.Rect,kill_rect_ver: pygame.Rect, direction: int) -> bool:
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
        self.max_velocity = upgrades["max velocity"]
        self.acceleration = upgrades["acceleration"]
        self.rotation_speed = upgrades["rotation speed"]
        self.grabber.extension_speed = upgrades["grabber speed"]
        self.can_slow_down = bool(upgrades["can slow down"])
        self.grabber.update_length(upgrades["grabber length"])

        self.max_shield = int(upgrades["shield"])
        self.shield = copy(self.max_shield)

    def bounce_off_meteorite(self, meteorite: Meteorite) -> None:
        if self.last_meteorite_hit is None:
            return

        surface_normal: pygame.Vector2 = -(self.position - meteorite.position).normalize()
        self.velocity = surface_normal * max(self.velocity.magnitude(), self.max_velocity / 2)
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

        self.shield_image.set_alpha(int(map_value_to_range(self.shield_visible,
                                                           0, 255, 0, self.shield_visibility_duration)))
        shield_rect: pygame.Rect = self.shield_image.get_rect(center=self.position)
        screen.blit(self.shield_image, shield_rect)
        self.shield_visible -= 1
