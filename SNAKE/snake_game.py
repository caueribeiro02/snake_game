import pygame
import random
import time
import sys

# Inicializa o Pygame
pygame.init()

# Configurações iniciais
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Cores
BACKGROUND = (15, 15, 15)
GRID_COLOR = (40, 40, 40)
SNAKE_COLOR = (50, 205, 50)
SNAKE_HEAD_COLOR = (34, 139, 34)
FOOD_COLOR = (220, 20, 60)
TEXT_COLOR = (255, 255, 255)

# Direções
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reinicia a cobrinha para o estado inicial"""
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow = False
        self.score = 0
        self.speed = 10
    
    def change_direction(self, direction):
        """Muda a direção da cobrinha"""
        # Impede movimento inverso (virar 180 graus)
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
    
    def move(self):
        """Move a cobrinha"""
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        new_x = (head_x + self.direction[0]) % GRID_WIDTH
        new_y = (head_y + self.direction[1]) % GRID_HEIGHT
        new_head = (new_x, new_y)
        
        # Verifica colisão com próprio corpo
        if new_head in self.body:
            return False
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            self.score += 10
            # Aumenta a velocidade a cada 5 comidas
            if self.score % 50 == 0 and self.speed < 20:
                self.speed += 1
        
        return True
    
    def eat(self, food):
        """Verifica se a cobrinha comeu a comida"""
        if self.body[0] == food:
            self.grow = True
            return True
        return False
    
    def draw(self, screen):
        """Desenha a cobrinha na tela"""
        for i, (x, y) in enumerate(self.body):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (30, 30, 30), rect, 1)

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)
        self.type = random.choice(['normal', 'special'])
        self.spawn_time = time.time()
    
    def generate_position(self, snake_body):
        """Gera uma posição aleatória que não colide com a cobrinha"""
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), 
                       random.randint(0, GRID_HEIGHT - 1))
            if position not in snake_body:
                return position
    
    def draw(self, screen):
        """Desenha a comida na tela"""
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        
        if self.type == 'special':
            # Comida especial - pisca
            if int(time.time() * 5) % 2 == 0:
                pygame.draw.rect(screen, (255, 215, 0), rect)  # Dourado
            else:
                pygame.draw.rect(screen, (255, 165, 0), rect)  # Laranja
        else:
            pygame.draw.rect(screen, FOOD_COLOR, rect)
        
        pygame.draw.rect(screen, (30, 30, 30), rect, 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Game - Python 🐍')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 24)
        self.big_font = pygame.font.SysFont('arial', 48, bold=True)
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.game_over = False
        self.paused = False
    
    def draw_grid(self):
        """Desenha a grade do jogo"""
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y))
    
    def draw_score(self):
        """Desenha a pontuação na tela"""
        score_text = self.font.render(f'Score: {self.snake.score}', True, TEXT_COLOR)
        speed_text = self.font.render(f'Speed: {self.snake.speed}', True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(speed_text, (10, 40))
    
    def draw_game_over(self):
        """Desenha a tela de game over"""
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BACKGROUND)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.big_font.render('GAME OVER', True, (255, 50, 50))
        score_text = self.font.render(f'Score Final: {self.snake.score}', True, TEXT_COLOR)
        restart_text = self.font.render('Pressione R para reiniciar', True, TEXT_COLOR)
        quit_text = self.font.render('Pressione Q para sair', True, TEXT_COLOR)
        
        self.screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
        self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        self.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 40))
        self.screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 70))
    
    def draw_pause(self):
        """Desenha a tela de pausa"""
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BACKGROUND)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.big_font.render('PAUSADO', True, (255, 255, 0))
        continue_text = self.font.render('Pressione P para continuar', True, TEXT_COLOR)
        
        self.screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 30))
        self.screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 30))
    
    def handle_events(self):
        """Lida com os eventos do jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.snake.reset()
                        self.food = Food(self.snake.body)
                        self.game_over = False
                    elif event.key == pygame.K_q:
                        return False
                
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                
                elif not self.paused:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
        
        return True
    
    def update(self):
        """Atualiza o estado do jogo"""
        if self.paused or self.game_over:
            return
        
        # Verifica se a comida especial expirou
        if self.food.type == 'special' and time.time() - self.food.spawn_time > 5:
            self.food = Food(self.snake.body)
        
        # Move a cobrinha e verifica colisões
        if not self.snake.move():
            self.game_over = True
            return
        
        # Verifica se comeu a comida
        if self.snake.eat(self.food.position):
            # Pontuação extra para comida especial
            if self.food.type == 'special':
                self.snake.score += 20
            self.food = Food(self.snake.body)
    
    def draw(self):
        """Desenha tudo na tela"""
        self.screen.fill(BACKGROUND)
        self.draw_grid()
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.draw_score()
        
        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_pause()
        
        pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.snake.speed)
        
        pygame.quit()
        sys.exit()

# Instruções iniciais
print("🐍 Snake Game Iniciando...")
print("=" * 40)
print("Controles:")
print("↑ ↓ ← → - Mover a cobrinha")
print("P - Pausar/Continuar")
print("R - Reiniciar (após game over)")
print("Q - Sair (após game over)")
print("=" * 40)
print("Dica: Comida dourada vale mais pontos!")
print("Divirta-se! 🎮")

# Inicia o jogo
if __name__ == "__main__":
    game = Game()
    game.run()