import pygame
import noise
import sys
import random

# Initialize pygame
pygame.init()

# Maze settings
CELL_SIZE = 6
COLS, ROWS = 100, 100
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
THRESHOLD = 0.1  # Lower = more passage

# Colors
WALL_COLOR = (0, 0, 0)
PASSAGE_COLOR = (220, 220, 220)  # Light gray

# Display setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Perlin Noise Maze")

# Generate random offset for perlin noise to make each run unique
x_offset = random.uniform(0, 1000)
y_offset = random.uniform(0, 1000)

def draw_maze():
    scale = 20.0
    for y in range(ROWS):
        for x in range(COLS):
            nx = (x + x_offset) / scale
            ny = (y + y_offset) / scale
            value = noise.pnoise2(nx, ny, octaves=1)

            if value > THRESHOLD:
                color = PASSAGE_COLOR
            else:
                color = WALL_COLOR

            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)

    pygame.display.flip()

def main():
    draw_maze()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
