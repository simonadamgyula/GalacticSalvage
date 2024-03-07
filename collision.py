import pygame


class Collision:
    @staticmethod
    def circle_circle_collision(circle1_center: pygame.Vector2, circle1_radius: float,
                                circle2_center: pygame.Vector2, circle2_radius: float) -> bool:
        return circle1_center.distance_to(circle2_center) < circle1_radius + circle2_radius

    @staticmethod
    def rectangle_circle_collision(rect_center: pygame.Vector2, verticies: list[pygame.Vector2],
                                   circle_center: pygame.Vector2, radius: float) -> bool:
        closest_point: pygame.Vector2 = Collision.intersection_of_segment_rect(verticies,
                                                                               (rect_center, circle_center))

        if not closest_point:
            return True
        return closest_point.distance_to(circle_center) < radius

    @staticmethod
    def intersection_of_segment_rect(verticies: list[pygame.Vector2], segment: tuple[pygame.Vector2, pygame.Vector2]) \
            -> pygame.Vector2:
        for i in range(len(verticies)):
            intersection: None | pygame.Vector2 = \
                Collision.intersection_of_linesegments(segment, (verticies[i], verticies[i - 1]))
            if intersection:
                return intersection

    @staticmethod
    def intersection_of_linesegments(segment1: tuple[pygame.Vector2, pygame.Vector2],
                                     segment2: tuple[pygame.Vector2, pygame.Vector2]) -> None | pygame.Vector2:
        x1, y1 = segment1[0]
        x2, y2 = segment1[1]
        x3, y3 = segment2[0]
        x4, y4 = segment2[1]

        a: float = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        b: float = (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)
        c: float = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if c == 0:
            return

        t: float = a / c
        u: float = -b / c

        if t < 0 or t > 1 or u < 0 or u > 1:
            return

        return pygame.Vector2(x1 + t * (x2 - x1), y1 + t * (y2 - y1))
