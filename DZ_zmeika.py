import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Часы для контроля скорости
clock = pygame.time.Clock()

# Шрифт для счета
font = pygame.font.SysFont(None, 36)

class Snake:
    def __init__(self):
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (0, -CELL_SIZE)  # Начинаем движеся вверх
        self.length = 1

    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # Проверка выхода за границы
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT):
            return False  # Игра окончена

        # Проверка на столкновение с собой
        if new_head in self.positions[1:]:
            return False

        self.positions = [new_head] + self.positions[:-1]
        return True

    def grow(self):
        # Добавляем новую часть змейки
        self.positions.append(self.positions[-1])
        self.length += 1

    def change_direction(self, new_direction):
        # Предотвращаем разворот на 180 градусов
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, DARK_GREEN, rect)
            pygame.draw.rect(surface, GREEN, rect, 1)  # Обводка

class Food:
    def __init__(self, snake_positions):
        self.position = self.random_position(snake_positions)

    def random_position(self, snake_positions):
        while True:
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            if (x, y) not in snake_positions:
                return (x, y)

    def draw(self, surface):
        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, RED, rect)

def show_score(surface, score):
    score_surf = font.render(f"Счет: {score}", True, WHITE)
    surface.blit(score_surf, (10, 10))

def main():
    snake = Snake()
    food = Food(snake.positions)
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -CELL_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, CELL_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-CELL_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((CELL_SIZE, 0))
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            moved = snake.move()
            if not moved:
                # Конец игры
                game_over = True

            # Проверка съедания еды
            if snake.positions[0] == food.position:
                snake.grow()
                score += 1
                food = Food(snake.positions)

            # Рисуем
            screen.fill(BLACK)
            snake.draw(screen)
            food.draw(screen)
            show_score(screen, score)

            pygame.display.flip()
            clock.tick(5)  # Скорость змейки (10 кадров в секунду)
        else:
            # Игра окончена - показать сообщение
            game_over_surf = font.render("Игра окончена! Нажмите любую клавишу.", True, WHITE)
            rect = game_over_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(game_over_surf, rect)
            pygame.display.flip()

            # Ожидание нажатия клавиши для выхода
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()