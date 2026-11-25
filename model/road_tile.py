class RoadTile:
    """Représente une case logique de la grille d'un circuit."""

    def __init__(self, col: int, row: int):
        """Initialise une case à sa position (colonne, ligne) dans la grille.

        Args:
            col: Indice de colonne de la case.
            row: Indice de ligne de la case.
        """
        self.col = col
        self.row = row
