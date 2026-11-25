import pygame
from constants import TILE_SIZE
from model.circuit import Circuit
from model.road_tile import RoadTile


class CircuitView:
    """Gère le rendu graphique d'un circuit et de ses cases avec Pygame."""

    def __init__(self):
        """Initialise le cache des sprites de cases."""
        self._sprite_cache: dict[int, pygame.Surface] = {}

    def _get_tile_sprite(self, tile: RoadTile, tile_size: int = TILE_SIZE) -> pygame.Surface:
        """Retourne la surface Pygame associée à une case (avec mise en cache)."""
        if tile_size not in self._sprite_cache:
            surface = pygame.Surface((tile_size, tile_size))
            surface.fill((80, 80, 90))
            pygame.draw.rect(surface, (60, 60, 70), surface.get_rect(), 2)
            self._sprite_cache[tile_size] = surface
        return self._sprite_cache[tile_size]

    def draw(self, screen: pygame.Surface, circuit: Circuit) -> None:
        """Dessine l'ensemble des cases du circuit sur l'écran."""
        for row_idx, row in enumerate(circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = self._get_tile_sprite(tile, TILE_SIZE)
                screen.blit(sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))
