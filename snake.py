import pygame
import random
import asyncio

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED   = (200, 0, 0)

# Game speed (frames per second)
FPS = 30

# Screen Setup
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

move_delay = 3

font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 48)

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

def move_snake(snake, direction, food, score):
    head_x, head_y = snake[0]
    dir_x, dir_y = direction
    new_head = (head_x + dir_x, head_y + dir_y)
    snake.insert(0, new_head)
    if new_head == food:
        food = spawn_food(snake)
        score += 1
    else:
        snake.pop()
    return snake, food, score

def spawn_food(snake):
    while True:
        x = random.randrange(0, WINDOW_WIDTH, CELL_SIZE)
        y = random.randrange(0, WINDOW_HEIGHT, CELL_SIZE)
        if (x, y) not in snake:
            return x, y

def draw_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def draw_game_over(score):
    screen.fill(BLACK)
    game_over_text = large_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Auto-restarting...", True, WHITE)
    screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 300))
    screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 360))
    pygame.display.flip()

def draw_food(food):
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

def check_collision(snake):
    head = snake[0]
    if head[0] < 0 or head[0] >= WINDOW_WIDTH:
        return True
    if head[1] < 0 or head[1] >= WINDOW_HEIGHT:
        return True
    if head in snake[1:]:
        return True
    return False

async def main():
    snake = [(300, 300), (280, 300), (260, 300)]
    direction = (CELL_SIZE, 0)
    food = spawn_food(snake)
    score = 0
    move_counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        move_counter += 1
        if move_counter >= move_delay:
            snake, food, score = move_snake(snake, direction, food, score)
            move_counter = 0

        if check_collision(snake):
            draw_game_over(score)
            await asyncio.sleep(2)  # Show game over for 2 seconds then reset
            snake = [(300, 300), (280, 300), (260, 300)]
            direction = (CELL_SIZE, 0)
            food = spawn_food(snake)
            score = 0
            move_counter = 0
        else:
            screen.fill(BLACK)
            draw_snake(snake)
            draw_food(food)
            draw_score(score)
            pygame.display.flip()

        clock.tick(FPS)
        await asyncio.sleep(0)

asyncio.run(main())