TERRAIN_PROPERTIES: dict[str, dict[str, float]] = {
    "road": {
        "traction": 1.0,
        "drift_threshold": 25.0,
        "drift_friction": 0.85,
    },
    "grass": {
        "traction": 0.75,
        "drift_threshold": 15.0,
        "drift_friction": 0.60,
    },
    "dirt": {
        "traction": 0.65,
        "drift_threshold": 10.0,
        "drift_friction": 0.40,
    },
    "ice": {
        "traction": 0.30,
        "drift_threshold": 3.0,
        "drift_friction": 0.05,
    },
    "void": {
        "traction": 0.0,
        "drift_threshold": 0.0,
        "drift_friction": 0.0,
    },
}


class RoadTile:
    """Représente une case logique de la grille d'un circuit avec ses propriétés physiques."""

    def __init__(self, col: int, row: int, terrain: str = "road"):
        """Initialise une case à sa position (colonne, ligne) et charge ses coefficients.

        Args:
            col: Indice de colonne de la case.
            row: Indice de ligne de la case.
            terrain: Type de terrain ('road', 'grass', 'dirt', 'ice', 'void').

        Raises:
            ValueError: Si le type de terrain n'existe pas dans TERRAIN_PROPERTIES.
        """
        if terrain not in TERRAIN_PROPERTIES:
            raise ValueError(f"Type de terrain inconnu : {terrain}")

        self.col = col
        self.row = row
        self.terrain = terrain

        props = TERRAIN_PROPERTIES[terrain]
        self.traction: float = props["traction"]
        self.drift_threshold: float = props["drift_threshold"]
        self.drift_friction: float = props["drift_friction"]

    def is_void(self) -> bool:
        """Indique si la case correspond à du vide."""
        return self.terrain == "void"