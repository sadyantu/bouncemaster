import pygame
import sys
import json

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game settings
WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
BALL_SIZE = 15
PADDLE_SPEED = 6
BALL_SPEED_X, BALL_SPEED_Y = 4, 4
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
GREEN = (0, 255, 128)
RED = (255, 64, 64)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bounce Master')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 16)

# Music settings
music_enabled = True
try:
    # Try to load background music (you can add your own music file)
    pygame.mixer.music.load('background_music.mp3')  # Add your music file here
    pygame.mixer.music.set_volume(0.5)
except:
    print("No background music file found. Add 'background_music.mp3' to enable music.")

# Sound effects
try:
    hit_sound = pygame.mixer.Sound('hit.wav')  # Add your sound file here
    hit_sound.set_volume(0.3)
except:
    hit_sound = None
    print("No hit sound file found. Add 'hit.wav' to enable sound effects.")

# Achievement system
ACHIEVEMENTS = {
    1: {"name": "First Hit", "description": "Score your first point", "color": GREEN},
    5: {"name": "Beginner", "description": "Score 5 points", "color": YELLOW},
    10: {"name": "Amateur", "description": "Score 10 points", "color": ORANGE},
    25: {"name": "Pro", "description": "Score 25 points", "color": RED},
    50: {"name": "Master", "description": "Score 50 points", "color": BLUE},
    100: {"name": "Legend", "description": "Score 100 points", "color": GREEN},
    200: {"name": "Unstoppable", "description": "Score 200 points", "color": YELLOW}
}

def load_achievements():
    try:
        with open('achievements.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_achievements(achievements):
    with open('achievements.json', 'w') as f:
        json.dump(achievements, f)

def check_achievements(score, earned_achievements):
    new_achievements = []
    for milestone, achievement in ACHIEVEMENTS.items():
        if score >= milestone and achievement["name"] not in earned_achievements:
            new_achievements.append(achievement["name"])
            earned_achievements.append(achievement["name"])
    return new_achievements, earned_achievements

def show_achievement_popup(achievement_name, color):
    # Show achievement popup for 3 seconds
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 3000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Achievement popup
        popup_width, popup_height = 300, 100
        popup_x = (WIDTH - popup_width) // 2
        popup_y = (HEIGHT - popup_height) // 2
        
        pygame.draw.rect(screen, color, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(screen, WHITE, (popup_x, popup_y, popup_width, popup_height), 3)
        
        # Achievement text
        title_text = font.render("ACHIEVEMENT UNLOCKED!", True, WHITE)
        achievement_text = font.render(achievement_name, True, WHITE)
        
        screen.blit(title_text, (popup_x + (popup_width - title_text.get_width()) // 2, popup_y + 20))
        screen.blit(achievement_text, (popup_x + (popup_width - achievement_text.get_width()) // 2, popup_y + 50))
        
        pygame.display.flip()
        clock.tick(FPS)

def show_achievements_screen(earned_achievements):
    screen.fill(BLUE)
    title_text = font.render('ACHIEVEMENTS', True, YELLOW)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
    
    y_pos = 120
    for milestone, achievement in ACHIEVEMENTS.items():
        if achievement["name"] in earned_achievements:
            # Earned achievement
            color = achievement["color"]
            status = "✓ EARNED"
        else:
            # Locked achievement
            color = WHITE
            status = f"Locked ({milestone} points needed)"
        
        name_text = font.render(achievement["name"], True, color)
        desc_text = small_font.render(achievement["description"], True, WHITE)
        status_text = small_font.render(status, True, color)
        
        screen.blit(name_text, (50, y_pos))
        screen.blit(desc_text, (50, y_pos + 25))
        screen.blit(status_text, (50, y_pos + 40))
        
        y_pos += 70
    
    back_text = font.render('Press any key to go back', True, WHITE)
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 50))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def toggle_music():
    global music_enabled
    music_enabled = not music_enabled
    if music_enabled:
        try:
            pygame.mixer.music.play(-1)  # Loop music
        except:
            pass
    else:
        pygame.mixer.music.stop()

def main():
    # High score handling
    highscore_file = 'highscore.txt'
    try:
        with open(highscore_file, 'r') as f:
            high_score = int(f.read())
    except:
        high_score = 0

    # Load achievements
    earned_achievements = load_achievements()

    # Home screen menu
    menu_options = ['Play Game', 'High Score', 'Achievements', 'Music: ON' if music_enabled else 'Music: OFF', 'Instructions', 'Quit']
    selected_option = 0
    menu_running = True
    
    while menu_running:
        screen.fill(BLUE)
        
        # Title
        title_text = font.render('BOUNCE MASTER', True, YELLOW)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        
        # Menu options
        for i, option in enumerate(menu_options):
            color = GREEN if i == selected_option else WHITE
            text = font.render(option, True, color)
            y_pos = 150 + i * 50
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_pos))
        
        # Instructions at bottom
        instruction_text = font.render('Use UP/DOWN arrows to navigate, ENTER to select', True, WHITE)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Play Game
                        menu_running = False
                        play_game(high_score, highscore_file, earned_achievements)
                        return main()  # Return to menu after game
                    elif selected_option == 1:  # High Score
                        show_high_score(high_score)
                    elif selected_option == 2:  # Achievements
                        show_achievements_screen(earned_achievements)
                    elif selected_option == 3:  # Music Toggle
                        toggle_music()
                        menu_options[3] = 'Music: ON' if music_enabled else 'Music: OFF'
                    elif selected_option == 4:  # Instructions
                        show_instructions()
                    elif selected_option == 5:  # Quit
                        pygame.quit()
                        sys.exit()

def show_high_score(high_score):
    screen.fill(BLUE)
    title_text = font.render('HIGH SCORE', True, YELLOW)
    score_text = font.render(f'{high_score}', True, GREEN)
    back_text = font.render('Press any key to go back', True, WHITE)
    
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 200))
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 100))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def show_instructions():
    screen.fill(BLUE)
    title_text = font.render('INSTRUCTIONS', True, YELLOW)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
    
    instructions = [
        'Use UP/DOWN arrow keys to move your paddle',
        'Hit the ball with your paddle to score points',
        'Don\'t let the ball pass your paddle!',
        'Try to beat your high score!',
        'Press SPACEBAR to pause the game',
        'Earn achievements by reaching score milestones!',
        'Ball speed increases every 10 points!',
        'Toggle music in the main menu'
    ]
    
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, WHITE)
        y_pos = 120 + i * 40
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_pos))
    
    back_text = font.render('Press any key to go back', True, WHITE)
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 100))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def play_game(high_score, highscore_file, earned_achievements):
    # Start background music
    if music_enabled:
        try:
            pygame.mixer.music.play(-1)  # Loop music
        except:
            pass
    
    # Paddle position
    paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    # Ball position and velocity
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_vel_x = -BALL_SPEED_X
    ball_vel_y = BALL_SPEED_Y
    score = 0
    speed_level = 1
    base_speed_x = BALL_SPEED_X
    base_speed_y = BALL_SPEED_Y
    running = True
    paused = False

    # Show start message
    screen.fill(BLUE)
    start_text = font.render('Press any key to start the game', True, YELLOW)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
        
        if paused:
            # Show pause screen
            screen.fill(BLUE)
            pause_text = font.render('PAUSED', True, YELLOW)
            resume_text = font.render('Press SPACEBAR to resume', True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 + 10))
            pygame.display.flip()
            continue
        
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and paddle_y > 0:
            paddle_y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and paddle_y < HEIGHT - PADDLE_HEIGHT:
            paddle_y += PADDLE_SPEED
        # Ball movement
        ball_x += ball_vel_x
        ball_y += ball_vel_y
        # Ball collision with top/bottom
        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_vel_y *= -1
        # Ball collision with paddle
        if (ball_x <= PADDLE_WIDTH and
            paddle_y < ball_y + BALL_SIZE and
            ball_y < paddle_y + PADDLE_HEIGHT):
            ball_vel_x *= -1
            score += 1
            
            # Play hit sound
            if hit_sound:
                hit_sound.play()
            
            # Increase ball speed every 10 points
            new_speed_level = (score // 10) + 1
            if new_speed_level > speed_level:
                speed_level = new_speed_level
                # Update ball speed
                ball_vel_x = base_speed_x * speed_level if ball_vel_x > 0 else -base_speed_x * speed_level
                ball_vel_y = base_speed_y * speed_level if ball_vel_y > 0 else -base_speed_y * speed_level
            
            # Check for achievements
            new_achievements, earned_achievements = check_achievements(score, earned_achievements)
            if new_achievements:
                save_achievements(earned_achievements)
                for achievement_name in new_achievements:
                    for milestone, achievement in ACHIEVEMENTS.items():
                        if achievement["name"] == achievement_name:
                            show_achievement_popup(achievement_name, achievement["color"])
                            break
        
        # Ball out of bounds (game over)
        if ball_x < 0:
            if score > high_score:
                high_score = score
                with open(highscore_file, 'w') as f:
                    f.write(str(high_score))
            game_over_text = font.render(f'Game Over! Score: {score}', True, YELLOW)
            high_score_text = font.render(f'High Score: {high_score}', True, YELLOW)
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
            continue
        # Ball collision with right wall
        if ball_x > WIDTH - BALL_SIZE:
            ball_vel_x *= -1
        # Draw everything
        screen.fill(BLUE)
        pygame.draw.rect(screen, GREEN, (0, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.ellipse(screen, RED, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
        score_text = font.render(f'Score: {score}', True, YELLOW)
        high_score_text = font.render(f'High Score: {high_score}', True, YELLOW)
        speed_text = font.render(f'Speed Level: {speed_level}', True, ORANGE)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))
        screen.blit(speed_text, (10, 70))
        pygame.display.flip()
    
    # Stop music when game ends
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main() 