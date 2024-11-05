# import and initialize pygame
import pygame
import random
import os  # for saving high score
pygame.init()

# colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)

# set screen width and height
screen_width = 900
screen_height = 600

# creating window
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# set caption on screen
pygame.display.set_caption("Enhanced Snake Game")
pygame.display.update()

# clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# functions
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def plot_obstacles(gameWindow, color, obstacles, obstacle_size):
    for obs in obstacles:
        pygame.draw.rect(gameWindow, color, [obs[0], obs[1], obstacle_size, obstacle_size])

def welcome_screen():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233, 220, 229))
        text_screen("Welcome to Snake Game", black, 230, 250)
        text_screen("Press Space Bar to Play", black, 260, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

        pygame.display.update()
        clock.tick(60)

# Game loop
def game_loop():
    # Game-specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    food_x = random.randint(20, screen_width - 20)
    food_y = random.randint(20, screen_height - 20)
    score = 0
    init_velocity = 5
    snake_size = 20
    fps = 60
    high_score = 0

    # Check if high score file exists
    if not os.path.exists("high_score.txt"):
        with open("high_score.txt", "w") as f:
            f.write("0")

    with open("high_score.txt", "r") as f:
        high_score = int(f.read())

    # Obstacles
    obstacle_size = 30
    obstacles = [(random.randint(50, screen_width - 50), random.randint(50, screen_height - 50)) for _ in range(5)]

    while not exit_game:
        if game_over:
            gameWindow.fill(white)
            text_screen("Game Over! Press Enter to Restart", red, 100, 250)
            text_screen(f"High Score: {high_score}", red, 100, 300)

            with open("high_score.txt", "w") as f:
                f.write(str(high_score))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome_screen()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            # Snake eats the food
            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 10
                food_x = random.randint(20, screen_width - 20)
                food_y = random.randint(20, screen_height - 20)
                snk_length += 4
                if score > high_score:
                    high_score = score

                # Increase snake speed as score increases (level up)
                if score % 50 == 0:
                    init_velocity += 1

            gameWindow.fill(white)
            text_screen(f"Score: {score}  High Score: {high_score}", red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            # Plot obstacles
            plot_obstacles(gameWindow, green, obstacles, obstacle_size)

            # Move snake
            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            # Check for snake collision with obstacles
            for obs in obstacles:
                if abs(snake_x - obs[0]) < obstacle_size and abs(snake_y - obs[1]) < obstacle_size:
                    game_over = True

            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome_screen()
