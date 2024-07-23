import random
from collections import deque
from PIL import Image, ImageDraw

def create_maze(width, height):
    maze = [[1] * width for _ in range(height)]
    start_x, start_y = (0, 0)
    maze[start_y][start_x] = 0
    stack = [(start_x, start_y)]

    def is_valid_move(x, y):
        if x < 0 or x >= width or y < 0 or y >= height:
            return False
        return maze[y][x] == 1

    def get_neighbours(x, y):
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(directions)
        neighbours = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid_move(nx, ny):
                neighbours.append((nx, ny))
        return neighbours

    while stack:
        x, y = stack[-1]
        neighbours = get_neighbours(x, y)
        if neighbours:
            nx, ny = random.choice(neighbours)
            maze[ny][nx] = 0
            maze[y + (ny - y) // 2][x + (nx - x) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze

def set_start_and_end(maze, start, end):
    start_x, start_y = start
    end_x, end_y = end
    maze[start_y][start_x] = 'A'
    maze[end_y][end_x] = 'B'

def find_path_bfs(maze, start, end):
    width, height = len(maze[0]), len(maze)
    queue = deque([start])
    visited = set()
    parent = {}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited.add(start)

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            break
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] != 1 and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)

    path = []
    if (x, y) == end:
        while (x, y) != start:
            path.append((x, y))
            x, y = parent[(x, y)]
        path.append(start)
        path.reverse()

    return path

def mark_path(maze, path):
    for x, y in path[1:-1]:  # Skip start 'A' and end 'B'
        maze[y][x] = '.'

def print_maze(maze):
    for row in maze:
        print(''.join(['#' if cell == 1 else ' ' if cell == 0 else cell for cell in row]))

def maze_to_image(maze, cell_size=10):
    width, height = len(maze[0]), len(maze)
    image_width, image_height = width * cell_size, height * cell_size
    image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(image)

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = 'black' if cell == 1 else 'white'
            if cell == 'A':
                color = 'green'
            elif cell == 'B':
                color = 'red'
            elif cell == '.':
                color = 'blue'
            draw.rectangle(
                [x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size],
                fill=color
            )

    return image

# Example usage
width, height = 21, 21
maze = create_maze(width, height)
start = (0, 0)
end = (width-1, height-1)
set_start_and_end(maze, start, end)
path = find_path_bfs(maze, start, end)
mark_path(maze, path)
print_maze(maze)
print(f"Distance from A to B: {len(path) - 1}")

# Generate and save the image
image = maze_to_image(maze)
image.save('maze.png')
image.show()  # This will open the image in the default image viewer
