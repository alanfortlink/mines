import random
from bomba import Bomba
from aberto import Aberto

class Jogo:
    def __init__(self, n = 10, m = 10):
        self.marcados = []
        self.n = n
        self.m = m

        # Cria matrix de n x m com None
        self.tabuleiro = [[None for __ in range(m)] for _ in range(n)]
        self.vizinhos = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
        self.popular()

    def ganhou(self):
        for linha in self.tabuleiro:
            for celula in linha:
                if celula is None:
                    return False

        return True

    def contar_bombas(self, i, j):
        contador = 0

        if self.valido(i, j) and type(self.tabuleiro[i][j]) is Bomba:
            contador += 1

        for (inc_i, inc_j) in self.vizinhos:
            iv = i + inc_i
            jv = j + inc_j

            if self.valido(iv, jv):
                if type(self.tabuleiro[iv][jv]) is Bomba:
                    contador += 1

        return contador

    def valido(self, i, j):
        return (i >= 0 and i < self.n and j >= 0 and j < self.m)
    
    def popular(self):
        p = 0.1
        numero_bombas = int(self.n * self.m * p)

        for _ in range(numero_bombas):
            linha = random.randint(0, self.n-1)
            coluna = random.randint(0, self.m-1)

            self.tabuleiro[linha][coluna] = Bomba()

    def marcar(self, linha, coluna):
        if self.valido(linha, coluna):
            if (linha, coluna) in self.marcados:
                self.marcados.remove((linha, coluna))
            else:
                self.marcados.append((linha, coluna))

    def clicar(self, linha, coluna):
        """
        @brief Processa o clique em uma célula

        @linha Linha em que o usuário clicou
        @coluna Coluna em que o usuário clicou

        @return False se o usuário clicou em uma bomba
        @return True se o usuário NÃO clicou em uma bomba
        """
        if (linha, coluna) in self.marcados:
            return True

        if type(self.tabuleiro[linha][coluna]) is Bomba:
            return False

        if self.tabuleiro[linha][coluna] is None:
            self.abrir(linha, coluna)

        self.tabuleiro[linha][coluna] = Aberto()

        return True

    def abrir(self, linha, coluna, checados = None):
        if checados is None:
            checados = []

        if not self.valido(linha, coluna):
            return

        if type(self.tabuleiro[linha][coluna]) is Bomba:
            return

        if (linha, coluna) in checados:
            return

        checados.append((linha, coluna))

        self.tabuleiro[linha][coluna] = Aberto()

        numero_bombas = self.contar_bombas(linha, coluna)
        if numero_bombas == 0:
            for inc_i, inc_j in self.vizinhos:
                self.abrir(linha + inc_i, coluna + inc_j, checados)
            
            

