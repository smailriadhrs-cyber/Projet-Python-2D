from constants import GameState, GRID_ROWS, GRID_COLS, COLOR_CAR_P1, COLOR_CAR_P2, TILE_SIZE
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
        self.circuit = Circuit.create_by_name("Circuit 2 - Chicane")
        self.spawn_cars()

    def spawn_cars(self) -> None:
        """Cree les deux voitures aux positions de depart 1 et 2 du circuit."""
        starts = self.circuit.get_start_positions()
        p1_x, p1_y = starts.get(1, (6.5 * TILE_SIZE, 9.5 * TILE_SIZE))
        p2_x, p2_y = starts.get(2, (6.5 * TILE_SIZE, 10.5 * TILE_SIZE))

        self.cars = [
            Car(p1_x, p1_y, start_angle=90.0, color=COLOR_CAR_P1),
            Car(p2_x, p2_y, start_angle=90.0, color=COLOR_CAR_P2),
        ]

    def update(self) -> None:
        """Met a jour les interactions terrain/blocs et la physique de chaque voiture."""
        if self.state != GameState.RACING or self.circuit is None:
            return

        for car in self.cars:
            tile = self.circuit.get_tile_at_pixel(car.x, car.y)

            if tile.is_void():
                car.reset_to_checkpoint()
                continue

            if tile.is_checkpoint():
                car.save_checkpoint(tile)

            if tile.is_boost():
                car.apply_boost()

            car.update_position(tile)