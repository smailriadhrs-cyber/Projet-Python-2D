import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_BRAKE, CAR_MAX_SPEED, CAR_MAX_REVERSE_SPEED,
    CAR_TURN_SPEED, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_AIR_FRICTION
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
        self.speed = min(self.speed + CAR_ACCELERATION, CAR_MAX_SPEED)
    def brake(self) -> None:
        """Freine la voiture, puis la fait reculer jusqu'a la vitesse max arriere."""
        self.speed = max(self.speed - CAR_BRAKE, CAR_MAX_REVERSE_SPEED)
    def turn_left(self) -> None:
        """Fait tourner la voiture a gauche si elle est en mouvement."""
        if abs(self.speed) < 0.05:
            return
        direction = 1 if self.speed > 0 else -1
        self.angle -= CAR_TURN_SPEED * direction

    def turn_right(self) -> None:
        """Fait tourner la voiture a droite si elle est en mouvement."""
        if abs(self.speed) < 0.05:
            return
        direction = 1 if self.speed > 0 else -1
        self.angle += CAR_TURN_SPEED * direction

    def apply_air_friction(self) -> None:
        """Applique les frottements de l'air proportionnels a la vitesse."""
        self.speed -= self.speed * CAR_AIR_FRICTION
        if abs(self.speed) < 0.02:
            self.speed = 0.0

    def update_position(self) -> None:
        """Applique les frottements de l'air puis deplace la voiture en 2D."""
        self.apply_air_friction()
        rad = math.radians(self.angle)
        self.x += -math.sin(rad) * self.speed
        self.y += math.cos(rad) * self.speed
        

    def build_sprite(self) -> pygame.Surface:
        """Construit l'image de la voiture avec un pare-brise indiquant l'avant."""
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH, CAR_HEIGHT), border_radius=5)
        pygame.draw.rect(surf, (180, 220, 255), (5, CAR_HEIGHT - 16, CAR_WIDTH - 10, 10), border_radius=2)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Retourne le sprite tourne selon l'angle actuel et son rectangle centre."""
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect