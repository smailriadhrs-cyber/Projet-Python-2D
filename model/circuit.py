from model.road_tile import RoadTile
from constants import TILE_SIZE

# Légende des symboles : chaque lettre associe (terrain, bloc)
# Terrains : R = Route, G = Herbe, D = Terre, I = Glace, V = Vide
# Blocs (posés sur de la route) : 1 = Départ J1, 2 = Départ J2, C = Checkpoint, L = Arrivée, B = Boost
SYMBOL_LEGEND: dict[str, tuple[str, str | None]] = {
    "R": ("road", None),
    "G": ("grass", None),
    "D": ("dirt", None),
    "I": ("ice", None),
    "V": ("void", None),
    "1": ("road", "start_1"),
    "2": ("road", "start_2"),
    "C": ("road", "checkpoint"),
    "L": ("road", "finish"),
    "B": ("road", "boost"),
}

CIRCUIT_LAYOUTS: dict[str, list[str]] = {
    "Circuit 1 - Ovale": [
        "VVVVVVVVVVVVVVVV",
        "VRRRRRRCCRRRRBBV",
        "VRRRRRRCCRRRRRRV",
        "VRRRGGGGGGGGRRRV",
        "VCRRGVVVVVVGRRCV",
        "VCRRGVVVVVVGRRCV",
        "VRRRGVVVVVVGRRRV",
        "VRRRGVVVVVVGRRRV",
        "VRRRGGGGGGGGRRRV",
        "VRRRRR1LRRRRRRRV",
        "VRRRRR2LRRRRRRRV",
        "VVVVVVVVVVVVVVVV",
    ],
    "Circuit 2 - Chicane": [
        "VVVVVVVVVVVVVVVV",
        "VRRRRCCVVIIIIRRV",
        "VRRRRCCVVIIIIRRV",
        "VRRGGRRVVRRGGRRV",
        "VRRGGRRRRRRGGRRV",
        "VRRGGRRRRRRGGRRV",
        "VRRGGVVVVVVGGRCV",
        "VRRGGVVVVVVGGRCV",
        "VRRGGVVVVVVGGRRV",
        "VBRR1LDDDDDDRRRV",
        "VBRR2LDDDDDDRRRV",
        "VVVVVVVVVVVVVVVV",
    ],
    "Circuit 3 - Rallye Glace": [
        "VVVVVVVVVVVVVVVV",
        "VRRRRIIIICCBBRRV",
        "VRRRRIIIICCBBRRV",
        "VRRGGGGGGGGGGRRV",
        "VCCGVVVVVVVVGRRV",
        "VRRGVVVDDDDDDRRV",
        "VRRGVVVDDDDDDRRV",
        "VRRGVVVDDGGGGGVV",
        "VRRGVVVCCGVVVVVV",
        "VRR1LRRRRGVVVVVV",
        "VRR2LRRRRGVVVVVV",
        "VVVVVVVVVVVVVVVV",
    ],
}


class Circuit:
    """Représente un circuit de course sous forme d'une grille 2D de cases."""

    def __init__(self, grid: list[list[RoadTile]], name: str = "Circuit"):
        """Initialise le circuit à partir d'une grille de cases.

        Args:
            grid: Matrice 2D [ligne][colonne] contenant les instances de RoadTile.
            name: Nom du circuit.
        """
        self.grid = grid
        self.name = name
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    @classmethod
    def from_layout(cls, name: str, layout: list[str]) -> "Circuit":
        """Construit un circuit à partir d'une carte textuelle.

        Args:
            name: Nom du circuit.
            layout: Liste de lignes de caractères définis dans SYMBOL_LEGEND.

        Returns:
            Une instance de Circuit correspondant à la carte.
        """
        grid: list[list[RoadTile]] = []
        for row_idx, line in enumerate(layout):
            row: list[RoadTile] = []
            for col_idx, symbol in enumerate(line):
                terrain, block = SYMBOL_LEGEND.get(symbol, ("void", None))
                row.append(RoadTile(col=col_idx, row=row_idx, terrain=terrain, block=block))
            grid.append(row)
        return cls(grid=grid, name=name)

    @classmethod
    def get_available_circuits(cls) -> list[str]:
        """Retourne la liste des noms de circuits disponibles."""
        return list(CIRCUIT_LAYOUTS.keys())

    @classmethod
    def create_by_name(cls, name: str) -> "Circuit":
        """Crée et retourne un circuit prédéfini à partir de son nom.

        Args:
            name: Nom exact du circuit présent dans CIRCUIT_LAYOUTS.

        Raises:
            ValueError: Si aucun circuit ne porte ce nom.
        """
        if name not in CIRCUIT_LAYOUTS:
            raise ValueError(f"Circuit inconnu : {name}")
        return cls.from_layout(name, CIRCUIT_LAYOUTS[name])

    def get_tile(self, col: int, row: int) -> RoadTile:
        """Retourne la case aux coordonnées données, ou une case vide hors limites."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return RoadTile(col=col, row=row, terrain="void")

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile:
        """Retourne la case correspondant à une position en pixels (px, py)."""
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)

    def is_void_at_pixel(self, px: float, py: float) -> bool:
        """Indique si la position en pixels (px, py) est sur du vide ou hors carte."""
        return self.get_tile_at_pixel(px, py).is_void()

    def is_boost_at_pixel(self, px: float, py: float) -> bool:
        """Indique si la position en pixels (px, py) se trouve sur un bloc boost."""
        return self.get_tile_at_pixel(px, py).is_boost()

    def get_tiles_by_block(self, block_type: str) -> list[RoadTile]:
        """Retourne toutes les cases du circuit possédant le type de bloc demandé."""
        matching_tiles: list[RoadTile] = []
        for row in self.grid:
            for tile in row:
                if tile.block == block_type:
                    matching_tiles.append(tile)
        return matching_tiles

    def get_start_positions(self) -> dict[int, tuple[float, float]]:
        """Retourne les coordonnées en pixels (centre de case) des départs 1 et 2."""
        starts: dict[int, tuple[float, float]] = {}
        for player_num, block_name in ((1, "start_1"), (2, "start_2")):
            tiles = self.get_tiles_by_block(block_name)
            if tiles:
                tile = tiles[0]
                cx = (tile.col + 0.5) * TILE_SIZE
                cy = (tile.row + 0.5) * TILE_SIZE
                starts[player_num] = (cx, cy)
        return starts

    def is_valid(self) -> bool:
        """Vérifie que le circuit est rectangulaire et contient les blocs essentiels."""
        if self.rows == 0 or self.cols == 0:
            return False
        if any(len(row) != self.cols for row in self.grid):
            return False

        starts = self.get_start_positions()
        has_starts = 1 in starts and 2 in starts
        has_finish = len(self.get_tiles_by_block("finish")) > 0
        has_checkpoints = len(self.get_tiles_by_block("checkpoint")) > 0
        return has_starts and has_finish and has_checkpoints

    def pixel_width(self) -> int:
        """Retourne la largeur totale du circuit en pixels."""
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        """Retourne la hauteur totale du circuit en pixels."""
        return self.rows * TILE_SIZE