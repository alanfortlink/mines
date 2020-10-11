import pygame
from jogo import Jogo
from aberto import Aberto
from bomba import Bomba
from marcado import Marcado

class Tela:
    MARGEM_L = 0.10
    MARGEM_A = 0.10

    def __init__(self, largura, altura, n, m):
        self.largura = largura
        self.altura = altura
        self.n = n
        self.m = m

    def setup(self):
        pygame.init()
        self.acabou = False
        self.ganhou = False
        self.perdeu = False
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        self.jogo = Jogo(self.n, self.m)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.largura_celula = self.largura / self.m
        self.altura_celula = self.altura / self.n
        self.margem_largura = self.largura_celula * Tela.MARGEM_L
        self.margem_altura = self.altura_celula * Tela.MARGEM_A
        self.rodando = True
        
    def run(self):
        self.clicou_esquerdo = False
        self.clicou_direito = False

        while self.rodando:
            if not self.processar_entrada():
                self.acabou = True
                self.perdeu = True

            self.checar_vitoria()

            if self.acabou:
                if self.ganhou:
                    self.atualizar_tela_vitoria()
                elif self.perdeu:
                    self.atualizar_tela_derrota()
            else:
                self.atualizar_tela()

    def checar_vitoria(self):
        if self.jogo.ganhou():
            self.acabou = True
            self.ganhou = True


    def restart(self):
        self.acabou = False
        self.ganhou = False
        self.perdeu = False
        self.jogo = Jogo(self.n, self.m)

    def processar_entrada(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.rodando = False
                return True

        if pygame.mouse.get_pressed()[0]:
            if not self.clicou_esquerdo:
                self.clicou_esquerdo = True
                if self.acabou:
                    self.restart()
                else:
                    pos = pygame.mouse.get_pos()
                    i = int(pos[1] / self.altura_celula)
                    j = int(pos[0] / self.largura_celula)

                    if not self.jogo.clicar(i, j):
                        return False

        else:
            self.clicou_esquerdo = False

        if pygame.mouse.get_pressed()[2]:
            if not self.clicou_direito:
                self.clicou_direito = True
                if not self.acabou:
                    pos = pygame.mouse.get_pos()
                    i = int(pos[1] / self.altura_celula)
                    j = int(pos[0] / self.largura_celula)

                    self.jogo.marcar(i, j)

        else:
            self.clicou_direito = False

        return True

    def atualizar_tela(self):
        self.tela.fill((255, 255, 255))
        for i in range(self.n):
            for j in range(self.m):
                self.desenhar_item(i, j)

        pygame.display.update()
        return True

    def atualizar_tela_derrota(self):
        self.tela.fill((255, 0, 0))
        superficie = self.font.render("Voce perdeu. Clique para recomecar.", True, (0, 0, 0))
        self.tela.blit(superficie, dest=(30, 250))
        pygame.display.update()

    def atualizar_tela_vitoria(self):
        self.tela.fill((0, 0, 255))
        superficie = self.font.render("Voce ganhou. Clique para recomecar.", True, (0, 0, 0))
        self.tela.blit(superficie, dest=(30, 250))
        pygame.display.update()

    def desenhar_item(self, i, j):
        x = j * self.largura_celula
        y = i * self.altura_celula

        item = self.jogo.tabuleiro[i][j]

        contador_bombas = self.jogo.contar_bombas(i, j)

        if type(item) is Aberto:
            cor = (200, 200, 200)
        elif (i, j) in self.jogo.marcados:
            cor = (250, 0, 0)
        else:
            cor = (120, 120, 120)

        pygame.draw.rect(self.tela, cor, (x + self.margem_largura, y + self.margem_altura, self.largura_celula - self.margem_largura, self.altura_celula - self.margem_altura))

        if type(item) is Aberto and contador_bombas > 0:
            superficie = self.font.render(str(contador_bombas), True, (0, 0, 0))
            self.tela.blit(superficie, dest=(x + 3.6 * self.margem_largura, y + 3.0 * self.margem_altura))

    def stop(self):
        pass
