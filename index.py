import pygame
import sys
import random
import json

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird Clone')

# Set up game variables
gravity = 0.25
bird_movement = 0
bird_rect = pygame.Rect(100, 250, 40, 30)

shapes = []

game_start_time = pygame.time.get_ticks()
timer = 0
clock = pygame.time.Clock()

pause_button = pygame.Rect(10, 10, 100, 30)
pause_text = "Pause"

dropdown_menu = False
menu_buttons = {
    "Home": pygame.Rect(10, 50, 100, 30),
    "Options": pygame.Rect(10, 90, 100, 30),
    "Quit": pygame.Rect(10, 130, 100, 30),
}

game_state = "running"  # Possible states: "running", "paused", "home", "options"

home_buttons = {
    "Play": pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 40, 100, 30),
    "Options": pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 30),
}

game_state = "home"  # Possible states: "running", "paused", "home", "options"


#HANDLE HIGHSCORE (ALL)
def load_highscore():
    try:
        with open("highscore.json", "r") as file:
            return json.load(file)["highscore"]
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_highscore(highscore):
    with open("highscore.json", "w") as file:
        json.dump({"highscore": highscore}, file)
        
high_score = load_highscore()
if timer > high_score:
    high_score = timer
    save_highscore(high_score)
    
def display_highscore():
    font = pygame.font.Font(None, 36)
    text = font.render(f"High Score: {high_score:.1f}", 1, (255, 255, 255))
    screen.blit(text, (WIDTH - 320, 10))



def draw_bird():
    pygame.draw.rect(screen, (244, 134, 246), bird_rect)

def update_bird():
    global bird_movement
    bird_movement += gravity
    bird_rect.y += int(bird_movement)

def check_collision():
    global high_score
    if bird_rect.y >= HEIGHT - 30:
        return True
    for shape in shapes:
        if bird_rect.colliderect(shape):
            if timer > high_score:
                high_score = timer
                save_highscore(high_score)
            return True
    return False


def generate_shape():
    size = random.randint(10, 30)
    x = WIDTH
    y = random.randint(0, HEIGHT - size)
    return pygame.Rect(x, y, size, size)

def draw_shapes():
    for shape in shapes:
        pygame.draw.rect(screen, (135, 0, 198), shape)

def update_shapes():
    global shapes
    shapes = [shape.move(-5, 0) for shape in shapes]
    if shapes and shapes[0].x < -shapes[0].width:
        shapes.pop(0)
    if not shapes or shapes[-1].x < WIDTH - 150:
        shapes.append(generate_shape())

def display_timer():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Time: {timer:.1f}", 1, (255, 255, 255))
    screen.blit(text, (WIDTH - 150, 10))

def draw_pause_button():
    pygame.draw.rect(screen, (200, 200, 200), pause_button)
    font = pygame.font.Font(None, 24)
    text = font.render(pause_text, 1, (0, 0, 0))
    screen.blit(text, (pause_button.x + 10, pause_button.y + 5))

def draw_dropdown_menu():
    for name, button in menu_buttons.items():
        pygame.draw.rect(screen, (200, 200, 200), button)
        font = pygame.font.Font(None, 24)
        text = font.render(name, 1, (0, 0, 0))
        screen.blit(text, (button.x + 10, button.y + 5))

def draw_home_screen():
    font = pygame.font.Font(None, 48)
    title = font.render("Flappy Bird Clone", 1, (0, 0, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    for name, button in home_buttons.items():
        pygame.draw.rect(screen, (200, 200, 200), button)
        font = pygame.font.Font(None, 24)
        text = font.render(name, 1, (0, 0, 0))
        screen.blit(text, (button.x + 10, button.y + 5))

def handle_mouse_click(pos):
    global dropdown_menu, game_state
    if game_state == "home":
        for name, button in home_buttons.items():
            if button.collidepoint(pos):
                if name == "Play":
                    game_state = "running"
                elif name == "Options":
                    game_state = "options"
    elif game_state in ["running", "paused"]:
        if pause_button.collidepoint(pos):
            dropdown_menu = not dropdown_menu
            if game_state == "running":
                game_state = "paused"
            elif game_state == "paused":
                game_state = "running"
        elif dropdown_menu:
            for name, button in menu_buttons.items():
                if button.collidepoint(pos):
                    if name == "Home":
                        game_state = "home"
                    elif name == "Options":
                        game_state = "options"
                    elif name == "Quit":
                        pygame.quit()
                        sys.exit()

# ...

while True:
    screen.fill((255, 176, 159))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == "running":
                bird_movement = -7

        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click(event.pos)

    if game_state == "home":
        draw_home_screen()
    elif game_state == "running":
        draw_bird()
        draw_shapes()
        display_timer()
        display_highscore()

        update_bird()
        update_shapes()

        if check_collision():
            bird_movement = 0
            bird_rect.y = HEIGHT - 30
            game_start_time = pygame.time.get_ticks()
        else:
            timer = (pygame.time.get_ticks() - game_start_time) / 1000

    elif game_state == "paused":
        draw_bird()
        draw_shapes()
        display_timer()

    if game_state in ["running", "paused"]:
        draw_pause_button()

        if dropdown_menu:
            draw_dropdown_menu()

    pygame.display.update()
    clock.tick(60)
  

