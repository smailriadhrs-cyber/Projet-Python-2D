import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_BRAKE, CAR_MAX_SPEED, CAR_MAX_REVERSE_SPEED,
    CAR_TURN_SPEED, CAR_AIR_FRICTION, CAR_GRIP_FACTOR,
    CAR_DRIFT_FRICTION_FACTOR, CAR_DRIFT_SLOWDOWN_FACTOR,
    CAR_BOOST_ACCELERATION, CAR_BOOST_MAX_SPEED,
    CAR_WIDTH, CAR_HEIGHT, TILE_SIZE
)
from model.road_tile import RoadTile

class Car:
    """Represente une voiture, sa physique 2D (avec drift) et son affichage."""

    def __init__(
        self,
        start_x: float,
        start_y: float,
        start_angle: float = 90.0,
        color: tuple[int, int, int] = (220, 40, 40)
    ):
        """Place la voiture a sa position de depart en pixels avec sa couleur."""
        self.x: float = start_x
        self.y: float = start_y
        self.vx: float = 0.0
        self.vy: float = 0.0
        self.speed: float = 0.0
        self.angle: float = start_angle
        self.is_drifting: bool = False
        self.checkpoint_x: float = start_x
        self.checkpoint_y: float = start_y
        self.checkpoint_angle: float = start_angle
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
        """Accelere selon la traction du terrain sans couper un eventuel boost."""
        current_speed = math.hypot(self.vx, self.vy)
        if current_speed >= CAR_MAX_SPEED:
            return

        fx, fy = self.get_forward_vector()
        self.vx += fx * CAR_ACCELERATION * traction
        self.vy += fy * CAR_ACCELERATION * traction

        new_speed = math.hypot(self.vx, self.vy)
        if new_speed > CAR_MAX_SPEED:
            ratio = CAR_MAX_SPEED / new_speed
            self.vx *= ratio
            self.vy *= ratio
    def brake(self, traction: float = 1.0) -> None:
        """Freine puis recule selon la traction du terrain jusqu'a la vitesse max arriere."""
        fx, fy = self.get_forward_vector()
        self.vx -= fx * CAR_BRAKE * traction
        self.vy -= fy * CAR_BRAKE * traction

        v_forward = self.vx * fx + self.vy * fy
        if v_forward < CAR_MAX_REVERSE_SPEED:
            diff = CAR_MAX_REVERSE_SPEED - v_forward
            self.vx += fx * diff
            self.vy += fy * diff
    def apply_boost(self) -> None:
        """Donne un bonus d'acceleration lorsque la voiture passe sur un bloc boost."""
        fx, fy = self.get_forward_vector()
        self.vx += fx * CAR_BOOST_ACCELERATION
        self.vy += fy * CAR_BOOST_ACCELERATION

        total_speed = math.hypot(self.vx, self.vy)
        if total_speed > CAR_BOOST_MAX_SPEED:
            ratio = CAR_BOOST_MAX_SPEED / total_speed
            self.vx *= ratio
            self.vy *= ratio
    def save_checkpoint(self, tile: RoadTile) -> None:
        """Enregistre le centre de la case checkpoint comme point de reapparition."""
        self.checkpoint_x = (tile.col + 0.5) * TILE_SIZE
        self.checkpoint_y = (tile.row + 0.5) * TILE_SIZE
        self.checkpoint_angle = self.angle

    def reset_to_checkpoint(self) -> None:
        """Teleporte la voiture au dernier checkpoint avec une vitesse nulle."""
        self.x = self.checkpoint_x
        self.y = self.checkpoint_y
        self.angle = self.checkpoint_angle
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 0.0
        self.is_drifting = False
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

    def update_position(self, tile: RoadTile) -> None:
        """Met a jour le derapage, la vitesse et la position selon le terrain courant."""
        self.apply_air_friction()

        fx, fy = self.get_forward_vector()
        lx, ly = self.get_lateral_vector()

        v_forward = self.vx * fx + self.vy * fy
        v_lateral = self.vx * lx + self.vy * ly
        total_speed = math.hypot(self.vx, self.vy)

        # Calcul de l'ecart angulaire (en degres) entre capot et vitesse
        if total_speed > 0.05:
            slip_angle = math.degrees(math.atan2(abs(v_lateral), abs(v_forward)))
        else:
            slip_angle = 0.0

        # Declenchement et arret automatique du derapage selon le terrain
        if not self.is_drifting:
            if slip_angle > tile.drift_threshold and total_speed > 1.0:
                self.is_drifting = True
        else:
            if slip_angle < tile.drift_threshold * 0.5 or total_speed < 0.5:
                self.is_drifting = False

        if self.is_drifting:
            # Frottements du sol en derapage (forts sur route, quasi nuls sur glace)
            v_lateral *= (1 - tile.drift_friction * CAR_DRIFT_FRICTION_FACTOR)
            v_forward *= (1 - tile.drift_friction * CAR_DRIFT_SLOWDOWN_FACTOR)
        else:
            # En adherence, la vitesse laterale s'amortit rapidement
            v_lateral *= (1 - CAR_GRIP_FACTOR)

        self.vx = fx * v_forward + lx * v_lateral
        self.vy = fy * v_forward + ly * v_lateral

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