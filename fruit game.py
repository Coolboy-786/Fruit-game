import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60

# Setup Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Apples")

# Load Assets
basket_img = pygame.image.load("basket.png")
apple_img = pygame.image.load("apple.jpeg")
background_img = pygame.image.load("background.jpeg")  # Load background image
catch_sound = pygame.mixer.Sound("catch.mp3")  # Load sound effect
miss_sound = pygame.mixer.Sound("miss.mp3")

# Scale Images
basket_img = pygame.transform.scale(basket_img, (100, 50))
apple_img = pygame.transform.scale(apple_img, (30, 30))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Scale background

# Basket Class
class Basket:
    def __init__(self):
        self.x = WIDTH // 2 - 50
        self.y = HEIGHT - 60
        self.speed = 7
        self.width = 100
        self.height = 50

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed

    def draw(self):
        screen.blit(basket_img, (self.x, self.y))

# Apple Class
class Apple:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 30)
        self.y = 0
        self.speed = random.randint(3, 7)
        self.width = 30
        self.height = 30

    def fall(self):
        self.y += self.speed

    def draw(self):
        screen.blit(apple_img, (self.x, self.y))

    def check_collision(self, basket):
        # Collision detection
        if (self.x + self.width > basket.x and self.x < basket.x + basket.width and
            self.y + self.height > basket.y and self.y < basket.y + basket.height):
            return True
        return False

# Game Loop
basket = Basket()
apples = [Apple()]
running = True
clock = pygame.time.Clock()
score = 0  # Add a score counter
dropped_apples = 0  # Counter for missed apples
max_dropped = 3  # Max missed apples before game over

while running:
    screen.blit(background_img, (0, 0))  # Draw background
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        basket.move("left")
    if keys[pygame.K_RIGHT]:
        basket.move("right")

    for apple in apples:
        apple.fall()
        apple.draw()

        if apple.y > HEIGHT:  # If apple falls off the screen
            apples.remove(apple)
            apples.append(Apple())
            dropped_apples += 1  # Increase missed count
            miss_sound.play()  # Play miss sound

        if apple.check_collision(basket):  # If basket catches the apple
            apples.remove(apple)
            apples.append(Apple())
            score += 1  # Increase score
            catch_sound.play()  # Play catch sound

    basket.draw()

    # Display Score and Missed Apples
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    misses_text = font.render(f"Missed: {dropped_apples}/{max_dropped}", True, (255, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(misses_text, (10, 40))

    # Check for Game Over
    if dropped_apples >= max_dropped:
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
