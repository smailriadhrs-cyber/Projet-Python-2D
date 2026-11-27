import pygame
from constants import TILE_SIZE, COLOR_BG
from model.circuit import Circuit
from model.road_tile import RoadTile

TERRAIN_COLORS: dict[str, tuple[int, int, int]] = {
    "road": (70, 72, 82),
    "grass": (55, 145, 65),
    "dirt": (148, 96, 52),
    "ice": (165, 222, 248),
    "void": COLOR_BG,
}


class CircuitView:
    """Gère le rendu graphique détaillé d'un circuit et de ses cases avec Pygame."""

    def __init__(self):
        """Initialise le cache des sprites et la police pour les marqueurs de blocs."""
        self._sprite_cache: dict[tuple[str, str | None, int], pygame.Surface] = {}
        self._font_cache: dict[int, pygame.font.Font] = {}

    def _get_font(self, size: int) -> pygame.font.Font:
        """Retourne une police Pygame mise en cache pour une taille donnée."""
        if size not in self._font_cache:
            if not pygame.font.get_init():
                pygame.font.init()
            self._font_cache[size] = pygame.font.SysFont("arial", size, bold=True)
        return self._font_cache[size]

    def _draw_terrain_texture(self, surface: pygame.Surface, terrain: str, tile_size: int) -> None:
        """Dessine la couleur de base et un motif procédural selon le type de terrain."""
        color = TERRAIN_COLORS.get(terrain, COLOR_BG)
        surface.fill(color)

        if terrain == "void":
            return

        if terrain == "road":
            # Grain léger de bitume
            speckle_light = (82, 84, 95)
            speckle_dark = (58, 60, 68)
            for rx, ry, col in (
                (0.20, 0.25, speckle_light),
                (0.75, 0.30, speckle_dark),
                (0.45, 0.65, speckle_light),
                (0.80, 0.78, speckle_dark),
                (0.25, 0.80, speckle_dark),
            ):
                pygame.draw.circle(surface, col, (int(tile_size * rx), int(tile_size * ry)), 2)

        elif terrain == "grass":
            # Petites touffes d'herbe
            blade_color = (38, 118, 48)
            highlight = (78, 172, 86)
            for rx, ry in ((0.25, 0.35), (0.72, 0.28), (0.50, 0.72), (0.22, 0.80), (0.78, 0.78)):
                x, y = int(tile_size * rx), int(tile_size * ry)
                pygame.draw.line(surface, blade_color, (x, y), (x - 3, y - 6), 2)
                pygame.draw.line(surface, highlight, (x, y), (x + 3, y - 5), 2)

        elif terrain == "dirt":
            # Cailloux et texture terreuse
            pebble_dark = (118, 74, 38)
            pebble_light = (176, 124, 76)
            for rx, ry, r, col in (
                (0.24, 0.26, 3, pebble_dark),
                (0.68, 0.22, 2, pebble_light),
                (0.48, 0.54, 4, pebble_dark),
                (0.76, 0.70, 3, pebble_dark),
                (0.26, 0.76, 2, pebble_light),
            ):
                pygame.draw.circle(surface, col, (int(tile_size * rx), int(tile_size * ry)), r)

        elif terrain == "ice":
            # Reflets diagonaux glacés
            shine = (225, 248, 255)
            pygame.draw.line(surface, shine, (int(tile_size * 0.15), int(tile_size * 0.45)),
                             (int(tile_size * 0.45), int(tile_size * 0.15)), 3)
            pygame.draw.line(surface, shine, (int(tile_size * 0.35), int(tile_size * 0.82)),
                             (int(tile_size * 0.82), int(tile_size * 0.35)), 2)
            pygame.draw.line(surface, (195, 238, 252), (int(tile_size * 0.55), int(tile_size * 0.88)),
                             (int(tile_size * 0.88), int(tile_size * 0.55)), 2)

        # Bordure subtile pour délimiter les cases
        border_color = tuple(max(0, c - 18) for c in color)
        pygame.draw.rect(surface, border_color, surface.get_rect(), 1)

    def _draw_block_overlay(self, surface: pygame.Surface, block: str | None, tile_size: int) -> None:
        """Dessine le marqueur visuel d'un bloc spécial par-dessus le terrain."""
        if block is None:
            return

        if block == "finish":
            # Damier noir et blanc 4x4
            square = tile_size // 4
            for r in range(4):
                for c in range(4):
                    color = (245, 245, 245) if (r + c) % 2 == 0 else (25, 25, 30)
                    pygame.draw.rect(surface, color, (c * square, r * square, square, square))
            pygame.draw.rect(surface, (200, 200, 200), surface.get_rect(), 1)

        elif block == "boost":
            # Pad lumineux avec doubles chevrons
            margin = max(4, tile_size // 10)
            pad_rect = pygame.Rect(margin, margin, tile_size - 2 * margin, tile_size - 2 * margin)
            pygame.draw.rect(surface, (45, 45, 55), pad_rect, border_radius=8)
            pygame.draw.rect(surface, (255, 185, 0), pad_rect, width=2, border_radius=8)

            cy = tile_size // 2
            for offset_x, col in ((0.28, (255, 140, 0)), (0.52, (255, 225, 40))):
                x0 = int(tile_size * offset_x)
                x1 = int(tile_size * (offset_x + 0.18))
                y_top = int(tile_size * 0.26)
                y_bot = int(tile_size * 0.74)
                pygame.draw.lines(surface, col, False, [(x0, y_top), (x1, cy), (x0, y_bot)], 4)

        elif block == "checkpoint":
            # Cadre cyan + marqueur "C"
            margin = max(6, tile_size // 8)
            rect = pygame.Rect(margin, margin, tile_size - 2 * margin, tile_size - 2 * margin)
            pygame.draw.rect(surface, (0, 215, 255), rect, width=3, border_radius=6)
            label = self._get_font(tile_size // 2).render("C", True, (0, 215, 255))
            surface.blit(label, label.get_rect(center=(tile_size // 2, tile_size // 2)))

        elif block in ("start_1", "start_2"):
            # Emplacement de grille de départ avec numéro du joueur
            margin = max(6, tile_size // 8)
            is_p1 = block == "start_1"
            color = (235, 75, 75) if is_p1 else (75, 145, 250)
            text = "1" if is_p1 else "2"

            # Ligne de grille façon F1 (U ouvert)
            rect = pygame.Rect(margin, margin, tile_size - 2 * margin, tile_size - 2 * margin)
            pygame.draw.rect(surface, color, rect, width=3, border_radius=4)
            label = self._get_font(tile_size // 2).render(text, True, color)
            surface.blit(label, label.get_rect(center=(tile_size // 2, tile_size // 2)))

    def _get_tile_sprite(self, tile: RoadTile, tile_size: int = TILE_SIZE) -> pygame.Surface:
        """Retourne la surface Pygame associée à une case (avec mise en cache)."""
        key = (tile.terrain, tile.block, tile_size)
        if key not in self._sprite_cache:
            surface = pygame.Surface((tile_size, tile_size))
            self._draw_terrain_texture(surface, tile.terrain, tile_size)
            self._draw_block_overlay(surface, tile.block, tile_size)
            self._sprite_cache[key] = surface
        return self._sprite_cache[key]

    def draw(self, screen: pygame.Surface, circuit: Circuit) -> None:
        """Dessine l'ensemble des cases du circuit sur l'écran."""
        for row_idx, row in enumerate(circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = self._get_tile_sprite(tile, TILE_SIZE)
                screen.blit(sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))