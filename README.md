## Circuits, terrains et blocs

Les circuits sont représentés par des grilles 2D de 16×12 cases (`model/circuit.py`, `model/road_tile.py`) avec rendu procédural mis en cache (`view/circuit_view.py`).

### Circuits disponibles
- **Circuit 1 - Ovale** : circuit rapide idéal pour prendre en main les voitures.
- **Circuit 2 - Chicane** : virages techniques combinant route, herbe, terre et glace.
- **Circuit 3 - Rallye Glace** : tracé exigeant avec boosts menant vers une grande zone glacée et une section terre.

### Terrains et propriétés physiques
| Symbole | Terrain | Traction | Seuil de dérapage (°) | Frottement de dérapage |
| :---: | :--- | :---: | :---: | :---: |
| `R` | Route (`road`) | 1.00 | 25.0 | 0.85 |
| `G` | Herbe (`grass`) | 0.75 | 15.0 | 0.60 |
| `D` | Terre (`dirt`) | 0.65 | 10.0 | 0.40 |
| `I` | Glace (`ice`) | 0.30 | 3.0 | 0.05 |
| `V` | Vide (`void`) | 0.00 | 0.0 | 0.00 |

### Blocs spéciaux
- `1` / `2` : emplacements de départ des joueurs 1 et 2 (`get_start_positions()`).
- `L` : ligne d'arrivée (`finish`).
- `C` : checkpoints (`checkpoint`).
- `B` : dalles de boost (`boost`, `is_boost_at_pixel()`).# Projet-Python-2D
Développer en groupe un jeu de course de voitures en 2D pour deux joueurs sur un même clavier, combinant la physique de dérapage de Trackmania et les objets/bonus de Mario Kart.
