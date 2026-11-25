from model.road_tile import RoadTile
from constants import TILE_SIZE


class Circuit:
    """Représente un circuit de course sous forme d'une grille 2D de cases."""

    def __init__(self, grid: list[list[RoadTile]]):
        """Initialise le circuit à partir d'une grille de cases.

        Args:
            grid: Matrice 2D [ligne][colonne] contenant les instances de RoadTile.
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def get_tile(self, col: int, row: int) -> RoadTile | None:
        """Retourne la case aux coordonnées de grille données, ou None hors limites."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        """Retourne la case correspondant à une position en pixels (px, py)."""
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)

    def pixel_width(self) -> int:
        """Retourne la largeur totale du circuit en pixels."""
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        """Retourne la hauteur totale du circuit en pixels."""
        return self.rows * TILE_SIZE
