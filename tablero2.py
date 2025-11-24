# game.py
from NewBoard2 import Board
from Agent2 import RandomAgent

class Game:
    def __init__(self, size=6, mines=6):
        # conveniencia: pasar (size, size, mines)
        self.board = Board(size, size, mines)

    def play(self):
        """Modo humano por consola."""
        while True:
            print("Comandos:")
            print("   r x y   -> revelar")
            print("   f x y   -> marcar/desmarcar bandera")
            print("   q       -> salir")
            self.board.print_board()
            cmd = input(">>> ").strip().split()

            if len(cmd) == 0:
                continue

            if cmd[0] == "q":
                print("Juego terminado.")
                break

            if len(cmd) != 3:
                print("Comando inválido.")
                continue

            action, xs, ys = cmd[0], cmd[1], cmd[2]

            if not (xs.isdigit() and ys.isdigit()):
                print("Coordenadas inválidas.")
                continue

            x, y = int(xs), int(ys)

            if action == "f":
                self.board.grid[x][y].is_flagged = not self.board.grid[x][y].is_flagged

            elif action == "r":
                ok = self.board.reveal_cell(x, y)
                if not ok:
                    print("BOOM! Has perdido.")
                    self.board.print_board(show_mines=True)
                    break

            if self.board.check_win():
                print("¡Ganaste! No quedan celdas seguras.")
                self.board.print_board(show_mines=True)
                break

def run_minesweeper_game(size=6, mines=6, agent=None, verbose=True, max_turns=1000):
    """
    Ejecuta un juego controlado por 'agent' (instancia con método get_move(board_state)).
    Devuelve (result, turns) donde result es "GANADO"|"PERDIDO"|"ABORTADO"
    """
    board = Board(size, size, mines)
    if agent is None:
        agent = RandomAgent()

    turns = 0
    status = "JUGANDO"

    if verbose:
        print(f"--- Comenzando juego ({size}x{size}, {mines} minas) ---")

    while status == "JUGANDO" and turns < max_turns:
        board_state = board.get_agent_view()
        move = agent.get_move(board_state)
        if move is None:
            status = "ABORTADO"
            if verbose:
                print("Agente no encontró movimientos válidos.")
            break
        r, c = move
        if verbose:
            print(f"Turno {turns+1}: agente elige ({r},{c})")
        status = board.reveal(r, c)
        turns += 1

    if verbose:
        print("Resultado:", status, "en", turns, "turnos.")
        board.print_board(show_mines=True)

    return status, turns

if __name__ == "__main__":
    # modo humano
    g = Game(7, 7)
    g.play()