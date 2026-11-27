import pygame


MAPPING_P1 = {
    pygame.K_z: "accelerate",
    pygame.K_w: "accelerate",
    pygame.K_s: "brake",
    pygame.K_q: "left",
    pygame.K_a: "left",
    pygame.K_d: "right",
}

MAPPING_P2 = {
    pygame.K_UP:    "accelerate",
    pygame.K_DOWN:  "brake",
    pygame.K_LEFT:  "left",
    pygame.K_RIGHT: "right",
}


class InputHandler:
    """Lit les touches clavier des deux joueurs et les traduit en actions."""

    def __init__(self):
        """Initialise les tables de correspondance clavier pour les 2 joueurs."""
        self.mappings = [MAPPING_P1, MAPPING_P2]

    def get_inputs(self) -> list[dict]:
        """Retourne une liste de deux dictionnaires d'actions (Joueur 1 puis Joueur 2)."""
        keys = pygame.key.get_pressed()
        all_inputs = []

        for mapping in self.mappings:
            player_actions = {action: False for action in mapping.values()}
            for key, action in mapping.items():
                if keys[key]:
                    player_actions[action] = True
            all_inputs.append(player_actions)

        return all_inputs
