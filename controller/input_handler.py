import pygame


MAPPING = {
    pygame.K_UP:    "accelerate",
    pygame.K_DOWN:  "brake",
    pygame.K_LEFT:  "left",
    pygame.K_RIGHT: "right",
}


class InputHandler:
    """Lit les touches maintenues au clavier et les associe aux actions du jeu."""

    def __init__(self):
        """Initialise le dictionnaire de correspondance touches -> actions."""
        self.mapping = MAPPING

    def get_inputs(self) -> dict:
        """Retourne un dictionnaire indiquant si chaque action est active."""
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping.values()}

        for key, action in self.mapping.items():
            if keys[key]:
                p[action] = True

        return p
