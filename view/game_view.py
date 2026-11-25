import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel
from view.circuit_view import CircuitView


class GameView:
    """Gère l'affichage principal du jeu (menus et écran de course)."""

    def __init__(self, screen: pygame.Surface):
        """Initialise la vue principale avec la fenêtre Pygame."""
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)
        self.circuit_view = CircuitView()

    def draw(self, model: GameModel) -> None:
        """Dessine l'écran correspondant à l'état courant du modèle."""
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu(model)
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        pygame.display.flip()

    def _draw_menu(self, model: GameModel) -> None:
        """Affiche le menu principal."""
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        options = [("JOUER (Enter)", GameState.RACING),
                   ("QUITTER (Escape)", None)]
        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER,
                             rect, 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def _draw_racing(self, model: GameModel) -> None:
        """Affiche le circuit et la voiture pendant la course."""
        if model.circuit is None:
            return

        self.circuit_view.draw(self.screen, model.circuit)

        if model.car is not None:
            surf, rect = model.car.get_rotated_sprite()
            self.screen.blit(surf, rect)
