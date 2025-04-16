import pygame
import random
import sys

# Grid settings
CELL_SIZE = 20
COLS, ROWS = 21, 21  # Must be odd
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Colors
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (220, 220, 220)
PLAYER_COLOR = (50, 200, 50)
SOLUTION_COLOR = (100, 180, 255)

# Directions for maze generation and DFS
DIRS = [(0, -2), (0, 2), (-2, 0), (2, 0)]

# Initialize
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze with DFS Solver")
clock = pygame.time.Clock()

# Maze grid
maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
solution_path = []

def generate_maze(x=1, y=1):
    maze[y][x] = 1
    dirs = DIRS[:]
    random.shuffle(dirs)

    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 < nx < COLS - 1 and 0 < ny < ROWS - 1 and maze[ny][nx] == 0:
            maze[y + dy // 2][x + dx // 2] = 1
            generate_maze(nx, ny)

def is_walkable(x, y):
    return 0 <= x < COLS and 0 <= y < ROWS and maze[y][x] == 1

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            color = PATH_COLOR if maze[y][x] == 1 else WALL_COLOR
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_solution(path):
    for x, y in path:
        pygame.draw.rect(screen, SOLUTION_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_player(x, y):
    pygame.draw.rect(screen, PLAYER_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def dfs(start, end):
    stack = [start]
    visited = set()
    parent = {}
    
    while stack:
        current = stack.pop()
        if current == end:
            break
        if current in visited:
            continue
        visited.add(current)
        
        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if is_walkable(nx, ny) and (nx, ny) not in visited:
                parent[(nx, ny)] = (x, y)
                stack.append((nx, ny))
    
    # Reconstruct path
    path = []
    node = end
    while node != start:
        path.append(node)
        node = parent.get(node)
        if node is None:
            return []  # No path
    path.append(start)
    return path[::-1]

def main():
    generate_maze()

    # Player
    player_x, player_y = 1, 1
    end_x, end_y = COLS - 2, ROWS - 2

    # Find solution path
    global solution_path
    solution_path = dfs((player_x, player_y), (end_x, end_y))

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_maze()
        draw_solution(solution_path)
        draw_player(player_x, player_y)
        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]: dx = -1
        if keys[pygame.K_RIGHT]: dx = 1
        if keys[pygame.K_UP]: dy = -1
        if keys[pygame.K_DOWN]: dy = 1

        if dx != 0 or dy != 0:
            nx, ny = player_x + dx, player_y + dy
            if is_walkable(nx, ny):
                player_x, player_y = nx, ny

        pygame.time.delay(100)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
