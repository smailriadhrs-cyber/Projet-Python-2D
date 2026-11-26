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

VALID_BLOCKS: set[str | None] = {
    None,
    "start_1",
    "start_2",
    "checkpoint",
    "finish",
    "boost",
}


class RoadTile:
    """Représente une case logique de la grille d'un circuit avec terrain et bloc éventuel."""

    def __init__(self, col: int, row: int, terrain: str = "road", block: str | None = None):
        """Initialise une case à sa position (colonne, ligne) et charge ses propriétés.

        Args:
            col: Indice de colonne de la case.
            row: Indice de ligne de la case.
            terrain: Type de terrain ('road', 'grass', 'dirt', 'ice', 'void').
            block: Bloc spécial posé sur la case ('start_1', 'start_2', 'checkpoint', 'finish', 'boost' ou None).

        Raises:
            ValueError: Si le type de terrain ou de bloc n'est pas reconnu.
        """
        if terrain not in TERRAIN_PROPERTIES:
            raise ValueError(f"Type de terrain inconnu : {terrain}")
        if block not in VALID_BLOCKS:
            raise ValueError(f"Type de bloc inconnu : {block}")

        self.col = col
        self.row = row
        self.terrain = terrain
        self.block = block

        props = TERRAIN_PROPERTIES[terrain]
        self.traction: float = props["traction"]
        self.drift_threshold: float = props["drift_threshold"]
        self.drift_friction: float = props["drift_friction"]

    def is_void(self) -> bool:
        """Indique si la case correspond à du vide."""
        return self.terrain == "void"

    def is_boost(self) -> bool:
        """Indique si la case contient un bloc de boost."""
        return self.block == "boost"

    def is_finish(self) -> bool:
        """Indique si la case fait partie de la ligne d'arrivée."""
        return self.block == "finish"

    def is_checkpoint(self) -> bool:
        """Indique si la case fait partie d'un checkpoint."""
        return self.block == "checkpoint"