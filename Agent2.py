# agent.py
import random

class RandomAgent:
    """
    Elige al azar entre las celdas ocultas (valor 0 en get_agent_view).
    """
    def get_move(self, board_state):
        rows = len(board_state)
        cols = len(board_state[0]) if rows > 0 else 0

        valid_moves = []
        for r in range(rows):
            for c in range(cols):
                # asumimos: 0 = oculta, -1 = bandera, >0 = revelada con número (0 incluido si adyacente_mines==0)
                if board_state[r][c] == 0:
                    valid_moves.append((r, c))

        if not valid_moves:
            return None
        return random.choice(valid_moves)