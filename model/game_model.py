from constants import GameState, GRID_ROWS, GRID_COLS, COLOR_CAR_P1, COLOR_CAR_P2
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:
    """Contient l'etat global du jeu : ecran courant, circuit et voitures."""

    def __init__(self):
        """Initialise le modele sur le menu principal sans circuit charge."""
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []

    def load_circuit(self) -> None:
        """Construit le circuit et place les deux voitures sur leurs positions de depart."""
        grid = [[RoadTile(col=col_idx, row=row_idx)
                 for col_idx in range(GRID_COLS)] for row_idx in range(GRID_ROWS)]
        self.circuit = Circuit(grid=grid)
        self.spawn_cars()

    def spawn_cars(self) -> None:
        """Cree les deux voitures (Joueur 1 rouge, Joueur 2 bleue)."""
        self.cars = [
            Car(6, 1, color=COLOR_CAR_P1),
            Car(8, 1, color=COLOR_CAR_P2),
        ]

    def update(self) -> None:
        """Met a jour la physique de chaque voiture pendant la course."""
        if self.state != GameState.RACING or self.circuit is None:
            return
        for car in self.cars:
            car.update_position()