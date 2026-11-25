import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_BRAKE, CAR_MAX_SPEED, CAR_MAX_REVERSE_SPEED,
    CAR_WIDTH, CAR_HEIGHT, TILE_SIZE
)


class Car:
    """Represente une voiture, sa position, sa vitesse et son affichage."""

    def __init__(self, start_col: int, start_row: int):
        """Place la voiture au centre de la case de depart."""
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        """Augmente la vitesse sans depasser la vitesse maximale."""
        self.speed += min(self.speed + CAR_ACCELERATION, CAR_MAX_SPEED)
    def brake(self) -> None:
        """Freine la voiture, puis la fait reculer jusqu'a la vitesse max arriere."""
        self.speed = max(self.speed - CAR_BRAKE, CAR_MAX_REVERSE_SPEED)

    def update_position(self) -> None:
        """Met a jour la position de la voiture selon sa vitesse actuelle."""
        self.y += self.speed

    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
