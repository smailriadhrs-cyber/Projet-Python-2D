class RoadTile:
    """Représente une case logique de la grille d'un circuit."""

    def __init__(self, col: int, row: int, terrain: str = "road"):
        """Initialise une case à sa position (colonne, ligne) dans la grille.

        Args:
            col: Indice de colonne de la case.
            row: Indice de ligne de la case.
            terrain: Type de terrain de la case ("road", "void", etc.).
        """
        self.col = col
        self.row = row
        self.terrain = terrain

    def is_void(self) -> bool:
        """Indique si la case correspond à du vide."""
        return self.terrain == "void"
