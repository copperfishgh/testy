import pygame
import sys

# Initialize Pygame
pygame.init()

# Create window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("PNG Size Test")

# Colors
RED = (255, 0, 0)

# Load the PNG image
try:
    original_image = pygame.image.load("pngs/2x/wK.png")
except pygame.error as e:
    print(f"Could not load image: {e}")
    pygame.quit()
    sys.exit()

# Create scaled versions with smooth scaling
image_50 = pygame.transform.smoothscale(original_image, (50, 50))
image_100 = pygame.transform.smoothscale(original_image, (100, 100))
image_300 = pygame.transform.smoothscale(original_image, (300, 300))

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Fill screen with red background
    screen.fill(RED)

    # Draw images with spacing so they don't touch
    # 50x50 image at top left
    screen.blit(image_50, (50, 50))

    # 100x100 image at top right
    screen.blit(image_100, (200, 50))

    # 300x300 image at bottom center
    screen.blit(image_300, (250, 200))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()