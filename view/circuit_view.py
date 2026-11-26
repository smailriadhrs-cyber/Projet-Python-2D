import pygame
from constants import TILE_SIZE, COLOR_BG
from model.circuit import Circuit
from model.road_tile import RoadTile

TERRAIN_COLORS: dict[str, tuple[int, int, int]] = {
    "road": (75, 75, 85),
    "grass": (60, 150, 70),
    "dirt": (150, 100, 55),
    "ice": (165, 220, 245),
    "void": COLOR_BG,
}


class CircuitView:
    """Gère le rendu graphique d'un circuit et de ses cases avec Pygame."""

    def __init__(self):
        """Initialise le cache des sprites par couple (terrain, taille)."""
        self._sprite_cache: dict[tuple[str, int], pygame.Surface] = {}

    def _get_tile_sprite(self, tile: RoadTile, tile_size: int = TILE_SIZE) -> pygame.Surface:
        """Retourne la surface Pygame associée à une case (avec mise en cache)."""
        key = (tile.terrain, tile_size)
        if key not in self._sprite_cache:
            surface = pygame.Surface((tile_size, tile_size))
            color = TERRAIN_COLORS.get(tile.terrain, COLOR_BG)
            surface.fill(color)

            if tile.terrain != "void":
                border_color = tuple(max(0, c - 20) for c in color)
                pygame.draw.rect(surface, border_color, surface.get_rect(), 1)

            self._sprite_cache[key] = surface
        return self._sprite_cache[key]

    def draw(self, screen: pygame.Surface, circuit: Circuit) -> None:
        """Dessine l'ensemble des cases du circuit sur l'écran."""
        for row_idx, row in enumerate(circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = self._get_tile_sprite(tile, TILE_SIZE)
                screen.blit(sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))