import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_BRAKE, CAR_MAX_SPEED, CAR_MAX_REVERSE_SPEED,
    CAR_TURN_SPEED, CAR_AIR_FRICTION, CAR_DRIFT_THRESHOLD, CAR_DRIFT_FRICTION,
    CAR_WIDTH, CAR_HEIGHT, TILE_SIZE
)


class Car:
    """Represente une voiture, sa physique 2D (avec drift) et son affichage."""

    def __init__(
        self,
        start_col: int,
        start_row: int,
        color: tuple[int, int, int] = (220, 40, 40)
    ):
        """Place la voiture sur sa case de depart avec sa couleur."""
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.vx: float = 0.0
        self.vy: float = 0.0
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.is_drifting: bool = False
        self.color = color
        self.sprite = self.build_sprite()
    def get_forward_vector(self) -> tuple[float, float]:
        """Retourne le vecteur unitaire pointe vers l'avant de la voiture."""
        rad = math.radians(self.angle)
        return -math.sin(rad), math.cos(rad)
    def get_lateral_vector(self) -> tuple[float, float]:
        """Retourne le vecteur unitaire perpendiculaire a la voiture."""
        rad = math.radians(self.angle)
        return math.cos(rad), math.sin(rad)

    def accelerate(self, traction: float = 1.0) -> None:
        """Accelere dans la direction du capot sans depasser la vitesse maximale."""
        fx, fy = self.get_forward_vector()
        self.vx += fx * CAR_ACCELERATION * traction
        self.vy += fy * CAR_ACCELERATION * traction

        total_speed = math.hypot(self.vx, self.vy)
        if total_speed > CAR_MAX_SPEED:
            ratio = CAR_MAX_SPEED / total_speed
            self.vx *= ratio
            self.vy *= ratio
    def brake(self, traction: float = 1.0) -> None:
        """Freine la voiture puis la fait reculer jusqu'a la vitesse max arriere."""
        fx, fy = self.get_forward_vector()
        self.vx -= fx * CAR_BRAKE * traction
        self.vy -= fy * CAR_BRAKE * traction

        v_forward = self.vx * fx + self.vy * fy
        if v_forward < CAR_MAX_REVERSE_SPEED:
            diff = CAR_MAX_REVERSE_SPEED - v_forward
            self.vx += fx * diff
            self.vy += fy * diff
    def turn_left(self) -> None:
        """Fait tourner la voiture a gauche si elle est en mouvement."""
        if math.hypot(self.vx, self.vy) < 0.05:
            return
        fx, fy = self.get_forward_vector()
        v_forward = self.vx * fx + self.vy * fy
        direction = 1 if v_forward >= 0 else -1
        self.angle -= CAR_TURN_SPEED * direction
    def turn_right(self) -> None:
        """Fait tourner la voiture a droite si elle est en mouvement."""
        if math.hypot(self.vx, self.vy) < 0.05:
            return
        fx, fy = self.get_forward_vector()
        v_forward = self.vx * fx + self.vy * fy
        direction = 1 if v_forward >= 0 else -1
        self.angle += CAR_TURN_SPEED * direction

    def apply_air_friction(self) -> None:
        """Reduit la vitesse proportionnellement aux frottements de l'air."""
        self.vx *= (1 - CAR_AIR_FRICTION)
        self.vy *= (1 - CAR_AIR_FRICTION)
        if math.hypot(self.vx, self.vy) < 0.02:
            self.vx = 0.0
            self.vy = 0.0

    def update_position(
        self,
        drift_threshold: float = CAR_DRIFT_THRESHOLD,
        drift_friction: float = CAR_DRIFT_FRICTION
    ) -> None:
        """Met a jour l'etat de derapage, la vitesse et la position 2D."""
        self.apply_air_friction()
        fx, fy = self.get_forward_vector()
        lx, ly = self.get_lateral_vector()
        v_forward = self.vx * fx + self.vy * fy
        v_lateral = self.vx * lx + self.vy * ly
        total_speed = math.hypot(self.vx, self.vy)

        
        if not self.is_drifting:
            if abs(v_lateral) > drift_threshold and total_speed > 1.0:
                self.is_drifting = True
        else:
            if abs(v_lateral) < drift_threshold * 0.5 or total_speed < 0.5:
                self.is_drifting = False

        if self.is_drifting:
            v_lateral *= (1 - drift_friction)
            self.vx = fx * v_forward + lx * v_lateral
            self.vy = fy * v_forward + ly * v_lateral
        else:
            sign = 1 if v_forward >= 0 else -1
            self.vx = fx * total_speed * sign
            self.vy = fy * total_speed * sign
        self.x += self.vx
        self.y += self.vy
        self.speed = math.hypot(self.vx, self.vy)
        

    def build_sprite(self) -> pygame.Surface:
        """Construit l'image de la voiture avec sa couleur et son pare-brise."""
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, CAR_WIDTH, CAR_HEIGHT), border_radius=5)
        pygame.draw.rect(
            surf, (180, 220, 255), (5, CAR_HEIGHT - 16, CAR_WIDTH - 10, 10), border_radius=2
        )
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Retourne le sprite tourne selon l'angle actuel et son rectangle centre."""
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect