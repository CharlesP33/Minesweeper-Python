# Charles PINET
# 1.0

from argparse import ArgumentParser
from os import system
from random import randint
from re import split


class Square:
    def __init__(self, is_bomb, n=-1):
        """
        Cette méthode prend en paramètre si c'est une mine et le nombre de mines autour de la case
        et elle initialise la case
        """
        self.is_revealed = False
        self.is_bomb = is_bomb
        self.n = n

    def __str__(self):
        """
        Cette méthode surcharge la méthode str pour appeler la méthode draw
        """
        return self.draw()

    def draw(self):
        """
        Cette méthode montre comment afficher la case
        """
        if self.is_revealed:
            if self.is_bomb:
                return '*'
            else:
                return str(self.n)
        else:
            return ' '


class Grid:
    def __init__(self, size, bombs):
        """
        Cette méthode prend en paramètre la taille du plateau et le nombre de mines qu'il contiendra
        et elle initialise le plateau
        """
        self.size = size
        self.create_grid(bombs)

    def __str__(self):
        """
        Cette méthode surcharge la méthode str pour appeler la méthode display
        """
        self.display()
        return ''

    def add_bombs(self, bombs):
        """
        Cette méthode prend en paramètres le nombre de mines et les rajoutes au plateau
        """
        # ajout des mines
        for i in range(bombs):
            r = randint(2, self.size)
            c = randint(1, self.size)
            if not self.grid[r][c].is_bomb:
                self.grid[r][c] = Square(True)
            else:
                self.add_bombs(1)

    def add_numbers(self):
        """
        Cette méthode rajoute le nombre de bombes qui sont voisines aux cases
        """
        # ajout du nombre de mine voisine à chaque case
        for i in range(2, self.size + 2):
            for j in range(1, self.size + 1):
                if not self.grid[i][j].is_bomb:
                    for y in [-1, 0, 1]:
                        for x in [-1, 0, 1]:
                            if 1 < i + y < self.size + 2 and 0 < j + x < self.size + 1:
                                if self.grid[i + y][j + x].is_bomb:
                                    self.grid[i][j].n += 1

    def create_grid(self, bombs):
        """
        Cette méthode prend en paramètre le nombre de mines et créer le plateau
        """
        # création de la grille vide
        self.grid = [[] for i in range(self.size + 2)]
        # ajout des index des colonnes
        self.grid[0].append([str(i) for i in range(self.size)])
        # ajout des séparateurs
        self.grid[1].append("---" * (self.size + 1))

        if self.size < 11:
            for i in range(self.size):
                # ajout des index des lignes
                self.grid[i + 2].append(str(i))
                for j in range(self.size):
                    # ajout des cases
                    self.grid[i + 2].append(Square(False, 0))
        else:
            for i in range(10):
                # ajout des index des lignes
                self.grid[i + 2].append(str(i) + ' ')
                for j in range(self.size):
                    # ajout des cases
                    self.grid[i + 2].append(Square(False, 0))
            for i in range(10, self.size):
                # ajout des index des lignes
                self.grid[i + 2].append(str(i))
                for j in range(self.size):
                    # ajout des cases
                    self.grid[i + 2].append(Square(False, 0))

        self.add_bombs(bombs)

        # ajout des séparateurs
        self.grid.append(["---" * (self.size + 1)])

        self.add_numbers()

    def display(self):
        """
        Cette méthode montre le plateau
        """
        if self.size < 11:
            print('   ', end='')
        else:
            print('    ', end='')
        print(*self.grid[0][0], sep='  ')
        print(*self.grid[1])
        for i in range(2, len(self.grid) - 1):
            print(*self.grid[i], sep=" |", end=' |\n')
        print(*self.grid[len(self.grid) - 1])

    def reveal_zero(self, pos):
        """
        Cette méthode récursive prend en paramètre la position de la case pour révéler ses voisins
        """
        for y in [-1, 0, 1]:
            for x in [-1, 0, 1]:
                if 1 < pos[0] + y < self.size + 2 and 0 < pos[1] + x < self.size + 1:
                    if self.grid[pos[0] + y][pos[1] + x].n == 0 and not self.grid[pos[0] + y][pos[1] + x].is_revealed:
                        self.grid[pos[0] + y][pos[1] + x].is_revealed = True
                        self.reveal_zero([pos[0] + y, pos[1] + x])
                    self.grid[pos[0] + y][pos[1] + x].is_revealed = True

    def win(self):
        """
        Cette méthode vérifie si toute les cases sont révéler donc que le joueur à gagner
        """
        grid_reveal = []
        for i in range(2, self.size + 2):
            for j in range(1, self.size + 1):
                grid_reveal.append(self.grid[i][j].is_revealed or self.grid[i][j].is_bomb)
        return all(grid_reveal)

    def hit(self):
        """
        Cette méthode va révéler la case choisi puis va detecter si le jeu se termine
        """
        while True:
            try:
                raw = input("Où souhaitez-vous jouer ? Entrer ligne, colonne : ")
                r, c = split(",", raw, 2)
                r = int(r)
                c = int(c)
                self.grid[r + 2][c + 1].is_revealed = True
                break
            except ValueError:
                print("Veuilliez entrer deux nombres entiers")
            except IndexError:
                print("Veuillez entrer un nombre compris entre 0 et " + str(self.size - 1))

        if self.grid[r + 2][c + 1].n == 0 and not self.grid[r + 2][c + 1].is_bomb:
            self.reveal_zero([r + 2, c + 1])

        if self.grid[r + 2][c + 1].is_bomb:
            return 0
        elif self.win():
            return 1
        else:
            return -1

    def reveal_all(self):
        """
        Cette méthode va révéler toute les cases
        """
        for i in range(2, self.size + 2):
            for j in range(1, self.size + 1):
                self.grid[i][j].is_revealed = True


def clear_screen():
    """
    Cette fonction efface l'écran de son ancien affjchage
    """
    system('cls')


def play(size, bombs):
    """
    Cette fonction lance et fait tourner le jeu
    Elle prend en paramètres deux entiers : la taille et le nombre de mines que contiendra le plateau
    """
    g = Grid(size, bombs)
    while True:
        clear_screen()
        print(g)
        result = g.hit()
        if result == 0:
            clear_screen()
            g.reveal_all()
            print(g)
            print("Vous avez toucher une mine, dommage.")
            break
        if result == 1:
            clear_screen()
            print(g)
            print("Vous avez gagné. Bravo!")
            break


if __name__ == "__main__":
    # Création des arguments pour le cmd
    parser = ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help", action="help", help="Montre ce message et quitte")
    parser.add_argument("-s", "--size", type=int, help="Définir la taille du plateau, par défaut 10", default=10)
    parser.add_argument("-b", "--bombs", type=int, help="Définir le nombre de mines, par défaut 10", default=10)
    args = parser.parse_args()

    if args.size < 2:
        print("La taille du plateau doit être supérieur à 1")
    elif args.bombs >= args.size ** 2:
        print("Le nombre de bombes est trop élevé")
    else:
        # Lance le jeu
        play(args.size, args.bombs)
