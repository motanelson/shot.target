import pygame
import sys
import random

# Inicializar o Pygame
pygame.init()

# Configurações da janela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Tiro - Pontuação: 0")

# Cores
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Configurações do jogo
score = 0
target_width = WIDTH // 8  # Largura de cada divisão
target_height = 80
target_speed = 3
spawn_timer = 0
spawn_delay = 60  # Frames entre spawns de targets

# Lista para armazenar os targets
targets = []

class Target:
    def __init__(self):
        # Escolher uma posição horizontal aleatória entre as 8 divisões
        self.division = random.randint(0, 7)
        self.x = self.division * target_width
        self.y = -target_height
        self.width = target_width
        self.height = target_height
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.speed = target_speed
        
    def update(self):
        self.y += self.speed
        return self.y > HEIGHT  # Retorna True se o target saiu da tela
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Desenhar uma borda para melhor visualização
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        
    def check_hit(self, pos):
        x, y = pos
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)

# Função para desenhar as divisões
def draw_divisions():
    for i in range(1, 8):
        x = i * target_width
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT), 1)

# Função para atualizar o título da janela
def update_title():
    pygame.display.set_caption(f"Jogo de Tiro - Pontuação: {score}")

# Loop principal do jogo
clock = pygame.time.Clock()
running = True

while running:
    # Processar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo do mouse
                # Verificar se acertou em algum target
                for target in targets[:]:
                    if target.check_hit(event.pos):
                        targets.remove(target)
                        score += 100
                        update_title()
                        break
    
    # Atualizar spawn de targets
    spawn_timer += 1
    if spawn_timer >= spawn_delay:
        targets.append(Target())
        spawn_timer = 0
    
    # Atualizar targets
    for target in targets[:]:
        if target.update():  # Se o target saiu da tela
            targets.remove(target)
    
    # Desenhar
    screen.fill(YELLOW)  # Fundo amarelo
    
    # Desenhar divisões
    draw_divisions()
    
    # Desenhar targets
    for target in targets:
        target.draw()
    
    # Atualizar display
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

# Sair do Pygame
pygame.quit()
sys.exit()
