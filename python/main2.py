import pygame
import random
import sys

# Grid and display settings
CELL_SIZE = 20
COLS, ROWS = 21, 21  # must be odd for proper maze
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Colors
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (220, 220, 220)
PLAYER_COLOR = (50, 200, 50)

# Directions (dx, dy)
DIRS = [(0, -2), (0, 2), (-2, 0), (2, 0)]

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometric Maze with Player")
clock = pygame.time.Clock()

# Maze grid: 0 = wall, 1 = passage
maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]

def generate_maze(x=1, y=1):
    maze[y][x] = 1
    dirs = DIRS[:]
    random.shuffle(dirs)

    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 < nx < COLS-1 and 0 < ny < ROWS-1 and maze[ny][nx] == 0:
            maze[y + dy//2][x + dx//2] = 1  # remove wall in between
            generate_maze(nx, ny)

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            color = PATH_COLOR if maze[y][x] == 1 else WALL_COLOR
            pygame.draw.rect(screen, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_player(px, py):
    pygame.draw.rect(screen, PLAYER_COLOR, (px*CELL_SIZE, py*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def is_walkable(x, y):
    return 0 <= x < COLS and 0 <= y < ROWS and maze[y][x] == 1

def main():
    generate_maze()

    # Player starts at (1, 1)
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

        # Handle keys
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

        pygame.time.delay(100)  # control move speed

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
