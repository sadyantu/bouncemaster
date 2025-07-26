import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game settings
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 5

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_rect(screen, color, pos):
    rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

def random_food(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    
    # Set up font for score
    font = pygame.font.SysFont('Arial', 24)

    # Load sound (use a simple beep if no file)
    try:
        eat_sound = pygame.mixer.Sound('eat.wav')
    except:
        eat_sound = None

    # Start screen
    screen.fill(BLACK)
    start_text = font.render('Press any key to start', True, WHITE)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = RIGHT
    food = random_food(snake)
    score = 0

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT

        # Move snake
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        # Check collisions
        if (
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in snake
        ):
            print(f'Game Over! Your score: {score}')
            # Show Game Over on screen
            screen.fill(BLACK)
            over_text = font.render(f'Game Over! Score: {score}', True, RED)
            screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 2 - over_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait 2 seconds
            running = False
            continue
        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = random_food(snake)
            # Play sound
            if eat_sound:
                eat_sound.play()
            else:
                # Fallback beep
                pygame.mixer.music.load(pygame.mixer.Sound(buffer=b'\x00' * 1000))
        else:
            snake.pop()

        # Draw everything
        screen.fill(BLACK)
        draw_rect(screen, RED, food)
        for segment in snake:
            draw_rect(screen, GREEN, segment)
        # Draw score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main() 