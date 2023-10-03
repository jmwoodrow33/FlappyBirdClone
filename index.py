import pygame
import sys
import random
import json

# initialize
pygame.init()

# display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird Clone')

# game variables
gravity = 0.25
birdMovement = 0
birdRect = pygame.Rect(100, 250, 40, 30)

shapes = []

gameStartTime = pygame.time.get_ticks()
timer = 0
clock = pygame.time.Clock()

pauseButton = pygame.Rect(10, 10, 100, 30)
pauseText = "Pause"

# menu
dropdownMenu = False
menuButtons = {
    "Home": pygame.Rect(10, 50, 100, 30),
    "Options": pygame.Rect(10, 90, 100, 30),
    "Quit": pygame.Rect(10, 130, 100, 30),
}

gameState = "running"  # Possible states: "running", "paused", "home", "options"

homeButtons = {
    "Play": pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 40, 100, 30),
    "Options": pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 30),
}

gameState = "home"  # Possible states: "running", "paused", "home", "options"


# highscore
def loadHighscore():
    try:
        with open("highscore.json", "r") as file:
            return json.load(file)["highscore"]
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def saveHighscore(highscore):
    with open("highscore.json", "w") as file:
        json.dump({"highscore": highscore}, file)
        
highScore = loadHighscore()
if timer > highScore:
    highScore = timer
    saveHighscore(highScore)
    
def displayHighscore():
    font = pygame.font.Font(None, 36)
    text = font.render(f"High Score: {highScore:.1f}", 1, (255, 255, 255))
    screen.blit(text, (WIDTH - 320, 10))


# player elements
def drawBird():
    pygame.draw.rect(screen, (244, 134, 246), birdRect)

def updateBird():
    global birdMovement
    birdMovement += gravity
    birdRect.y += int(birdMovement)

# com elements
def checkCollision():
    global highScore
    if birdRect.y >= HEIGHT - 30:
        return True
    for shape in shapes:
        if birdRect.colliderect(shape):
            if timer > highScore:
                highScore = timer
                saveHighscore(highScore)
            return True
    return False


def generateShape():
    size = random.randint(10, 30)
    x = WIDTH
    y = random.randint(0, HEIGHT - size)
    return pygame.Rect(x, y, size, size)

def drawShapes():
    for shape in shapes:
        pygame.draw.rect(screen, (135, 0, 198), shape)

def updateShapes():
    global shapes
    shapes = [shape.move(-5, 0) for shape in shapes]
    if shapes and shapes[0].x < -shapes[0].width:
        shapes.pop(0)
    if not shapes or shapes[-1].x < WIDTH - 150:
        shapes.append(generateShape())

# timer/etc display
def display_timer():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Time: {timer:.1f}", 1, (255, 255, 255))
    screen.blit(text, (WIDTH - 150, 10))

def drawPauseButton():
    pygame.draw.rect(screen, (200, 200, 200), pauseButton)
    font = pygame.font.Font(None, 24)
    text = font.render(pauseText, 1, (0, 0, 0))
    screen.blit(text, (pauseButton.x + 10, pauseButton.y + 5))

def drawDropdownMenu():
    for name, button in menuButtons.items():
        pygame.draw.rect(screen, (200, 200, 200), button)
        font = pygame.font.Font(None, 24)
        text = font.render(name, 1, (0, 0, 0))
        screen.blit(text, (button.x + 10, button.y + 5))

def drawHomeScreen():
    font = pygame.font.Font(None, 48)
    title = font.render("Flappy Bird Clone", 1, (0, 0, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    for name, button in homeButtons.items():
        pygame.draw.rect(screen, (200, 200, 200), button)
        font = pygame.font.Font(None, 24)
        text = font.render(name, 1, (0, 0, 0))
        screen.blit(text, (button.x + 10, button.y + 5))

# interaction
def handleMouseClick(pos):
    global dropdownMenu, gameState
    if gameState == "home":
        for name, button in homeButtons.items():
            if button.collidepoint(pos):
                if name == "Play":
                    gameState = "running"
                elif name == "Options":
                    gameState = "options"
    elif gameState in ["running", "paused"]:
        if pauseButton.collidepoint(pos):
            dropdownMenu = not dropdownMenu
            if gameState == "running":
                gameState = "paused"
            elif gameState == "paused":
                gameState = "running"
        elif dropdownMenu:
            for name, button in menuButtons.items():
                if button.collidepoint(pos):
                    if name == "Home":
                        gameState = "home"
                    elif name == "Options":
                        gameState = "options"
                    elif name == "Quit":
                        pygame.quit()
                        sys.exit()


while True:
    screen.fill((255, 176, 159))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameState == "running":
                birdMovement = -7

        if event.type == pygame.MOUSEBUTTONDOWN:
            handleMouseClick(event.pos)

    if gameState == "home":
        drawHomeScreen()
    elif gameState == "running":
        drawBird()
        drawShapes()
        display_timer()
        displayHighscore()

        updateBird()
        updateShapes()

        if checkCollision():
            birdMovement = 0
            birdRect.y = HEIGHT - 30
            gameStartTime = pygame.time.get_ticks()
        else:
            timer = (pygame.time.get_ticks() - gameStartTime) / 1000

    elif gameState == "paused":
        drawBird()
        drawShapes()
        display_timer()

    if gameState in ["running", "paused"]:
        drawPauseButton()

        if dropdownMenu:
            drawDropdownMenu()

    pygame.display.update()
    clock.tick(60)
  

