# board.py
from Cell import Cell
import random

class Board:
    def __init__(self, size_x=6, size_y=6, mines=6):
        """
        Board indexed as self.grid[x][y], where:
         - x in [0..size_x-1] are rows
         - y in [0..size_y-1] are columns
        """
        self.size_x = size_x
        self.size_y = size_y
        self.mines = mines
        # initialize grid: grid[x][y]
        self.grid = [[Cell() for _ in range(size_y)] for _ in range(size_x)]
        self.place_mines()
        self.compute_adjacent_counts()

    def valid(self, x, y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def place_mines(self):
        all_positions = [(x, y) for x in range(self.size_x) for y in range(self.size_y)]
        positions = random.sample(all_positions, min(self.mines, len(all_positions)))
        for x, y in positions:
            self.grid[x][y].is_mine = True

    def compute_adjacent_counts(self):
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.grid[x][y].is_mine:
                    self.grid[x][y].adjacent_mines = -1
                    continue
                count = 0
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if self.valid(nx, ny) and self.grid[nx][ny].is_mine:
                            count += 1
                self.grid[x][y].adjacent_mines = count

    def reveal_cell(self, x, y):
        """
        Revela la celda (x,y). Devuelve:
          - False si hubo mina (explota)
          - True si revelación OK (incluye abrir región de ceros)
        """
        if not self.valid(x, y):
            # coordenada inválida
            return False

        cell = self.grid[x][y]

        if cell.is_flagged:
            # no revelar una celda marcada
            return True

        if cell.is_revealed:
            return True

        cell.is_revealed = True

        if cell.is_mine:
            return False

        # si es cero, expandir con flood-fill (usando visited local)
        if cell.adjacent_mines == 0:
            self.flood_fill(x, y, visited=set())

        return True

    def flood_fill(self, x, y, visited):
        """
        Expansión recursiva de celdas adyacentes a 0.
        'visited' es un set local para evitar re-procesos (DP / memo).
        """
        if (x, y) in visited:
            return
        visited.add((x, y))

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if not self.valid(nx, ny):
                    continue
                neighbor = self.grid[nx][ny]
                if not neighbor.is_revealed and not neighbor.is_mine:
                    neighbor.is_revealed = True
                    if neighbor.adjacent_mines == 0:
                        self.flood_fill(nx, ny, visited)

    def get_agent_view(self):
        """
        Devuelve la vista que verá el agente como una matriz (size_x x size_y):
         - -1 : celda marcada con bandera
         -  0 : celda oculta
         -  1..8 : celda revelada con ese número
         -  0 (también) : celda revelada con 0 (se podría diferenciar si se quisiera)
        """
        view = []
        for x in range(self.size_x):
            row = []
            for y in range(self.size_y):
                c = self.grid[x][y]
                if c.is_flagged:
                    row.append(-1)
                elif not c.is_revealed:
                    row.append(0)
                else:
                    # si se quiere distinguir 0 revelado, se puede devolver -2; por ahora devolvemos 0
                    row.append(c.adjacent_mines)
            view.append(row)
        return view

    def reveal(self, x, y):
        """
        Wrapper pensado para agentes:
         - retorna "PERDIDO" si explotó una mina
         - retorna "GANADO" si quedó todo revelado sin minas
         - retorna "JUGANDO" en caso contrario
        """
        ok = self.reveal_cell(x, y)
        if not ok:
            # explotó
            return "PERDIDO"
        if self.check_win():
            return "GANADO"
        return "JUGANDO"

    def check_win(self):
        """True si todas las celdas no-mina están reveladas."""
        for x in range(self.size_x):
            for y in range(self.size_y):
                c = self.grid[x][y]
                if not c.is_mine and not c.is_revealed:
                    return False
        return True

    def print_board(self, show_mines=False):
        """Imprime tablero en consola. show_mines=True revela minas visibles."""
        # header
        print("   " + " ".join(str(i) for i in range(self.size_y)))
        print("   " + "--" * self.size_y)
        for x in range(self.size_x):
            row = []
            for y in range(self.size_y):
                c = self.grid[x][y]
                if show_mines and c.is_mine:
                    row.append("*")
                else:
                    row.append(str(c))
            print(f"{x} | " + " ".join(row))
