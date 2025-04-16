import pygame
import noise
import random
import sys

# Grid and display settings
CELL_SIZE = 20
COLS, ROWS = 41, 41  # Odd for proper maze feel
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Colors
WALL_COLOR = (20, 20, 20)
PLAYER_COLOR = (50, 200, 50)

# Noise config
SCALE = 10.0
THRESHOLD = 0.05  # Lower = more wall, higher = more open space

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Noise Maze with Player")
clock = pygame.time.Clock()

# Maze grid
maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Random offset for unique maze each time
x_offset = random.uniform(0, 1000)
y_offset = random.uniform(0, 1000)

def generate_maze():
    for y in range(ROWS):
        for x in range(COLS):
            nx = (x + x_offset) / SCALE
            ny = (y + y_offset) / SCALE
            value = noise.pnoise2(nx, ny)
            if value > THRESHOLD:
                maze[y][x] = 1  # path
            else:
                maze[y][x] = 0  # wall

    # Ensure start is walkable
    maze[1][1] = 1

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            val = maze[y][x]
            if val == 1:
                # Use noise again for subtle shading effect
                nx = (x + x_offset) / SCALE
                ny = (y + y_offset) / SCALE
                brightness = int((noise.pnoise2(nx, ny) + 1) * 127)
                color = (brightness, brightness, brightness)
            else:
                color = WALL_COLOR

            pygame.draw.rect(screen, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_player(px, py):
    pygame.draw.rect(screen, PLAYER_COLOR, (px*CELL_SIZE, py*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def is_walkable(x, y):
    return 0 <= x < COLS and 0 <= y < ROWS and maze[y][x] == 1

def main():
    generate_maze()
    player_x, player_y = 1, 1

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_maze()
        draw_player(player_x, player_y)
        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movement handling
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
        elif keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1

        if dx != 0 or dy != 0:
            nx, ny = player_x + dx, player_y + dy
            if is_walkable(nx, ny):
                player_x, player_y = nx, ny

        pygame.time.delay(100)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
