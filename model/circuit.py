from model.road_tile import RoadTile
from constants import TILE_SIZE

# Légende des terrains :
# R = Route (road), G = Herbe (grass), D = Terre (dirt), I = Glace (ice), V = Vide (void)
TERRAIN_LEGEND: dict[str, str] = {
    "R": "road",
    "G": "grass",
    "D": "dirt",
    "I": "ice",
    "V": "void",
}

CIRCUIT_LAYOUTS: dict[str, list[str]] = {
    "Circuit 1 - Ovale": [
        "VVVVVVVVVVVVVVVV",
        "VRRRRRRRRRRRRRRV",
        "VRRRRRRRRRRRRRRV",
        "VRRRGGGGGGGGRRRV",
        "VRRRGVVVVVVGRRRV",
        "VRRRGVVVVVVGRRRV",
        "VRRRGVVVVVVGRRRV",
        "VRRRGVVVVVVGRRRV",
        "VRRRGGGGGGGGRRRV",
        "VRRRRRRRRRRRRRRV",
        "VRRRRRRRRRRRRRRV",
        "VVVVVVVVVVVVVVVV",
    ],
    "Circuit 2 - Chicane": [
        "VVVVVVVVVVVVVVVV",
        "VRRRRRRVVIIIIRRV",
        "VRRRRRRVVIIIIRRV",
        "VRRGGRRVVRRGGRRV",
        "VRRGGRRRRRRGGRRV",
        "VRRGGRRRRRRGGRRV",
        "VRRGGVVVVVVGGRRV",
        "VRRGGVVVVVVGGRRV",
        "VRRGGVVVVVVGGRRV",
        "VRRRRDDDDDDRRRRV",
        "VRRRRDDDDDDRRRRV",
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
            layout: Liste de lignes de caractères ('R', 'G', 'D', 'I', 'V').

        Returns:
            Une instance de Circuit correspondant à la carte.
        """
        grid: list[list[RoadTile]] = []
        for row_idx, line in enumerate(layout):
            row: list[RoadTile] = []
            for col_idx, symbol in enumerate(line):
                terrain = TERRAIN_LEGEND.get(symbol, "void")
                row.append(RoadTile(col=col_idx, row=row_idx, terrain=terrain))
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

    def pixel_width(self) -> int:
        """Retourne la largeur totale du circuit en pixels."""
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        """Retourne la hauteur totale du circuit en pixels."""
        return self.rows * TILE_SIZE