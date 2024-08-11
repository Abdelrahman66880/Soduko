import pygame

# Initialize the pygame
pygame.font.init()

# Set up the display window
window_size = 500
grid_size = 9
cell_size = window_size // grid_size
window = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Sudoku Game by DataFlair")

# Default Sudoku grid
default_grid = [
    [0, 0, 4, 0, 6, 0, 0, 0, 5],
    [7, 8, 0, 4, 0, 0, 0, 2, 0],
    [0, 0, 2, 6, 0, 1, 0, 7, 8],
    [6, 1, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 7, 5, 4, 0, 0, 6, 1],
    [0, 0, 1, 7, 5, 0, 9, 3, 0],
    [0, 7, 0, 3, 0, 0, 0, 1, 0],
    [0, 4, 0, 2, 0, 6, 0, 0, 7],
    [0, 2, 0, 0, 0, 7, 4, 0, 0],
]

# Fonts for rendering text
font_large = pygame.font.SysFont("comicsans", 40)
font_small = pygame.font.SysFont("comicsans", 20)

# Coordinates of the selected cell
selected_x = 0
selected_y = 0

# Current value to be filled in the cell
current_value = 0

def get_cell_coords(pos):
    """Get the coordinates of the cell from mouse position."""
    global selected_x, selected_y
    selected_x = pos[0] // cell_size
    selected_y = pos[1] // cell_size

def highlight_selected_cell():
    """Highlight the selected cell."""
    for k in range(2):
        pygame.draw.line(window, (0, 0, 0), (selected_x * cell_size - 3, (selected_y + k) * cell_size), 
                         (selected_x * cell_size + cell_size + 3, (selected_y + k) * cell_size), 7)
        pygame.draw.line(window, (0, 0, 0), ((selected_x + k) * cell_size, selected_y * cell_size), 
                         ((selected_x + k) * cell_size, selected_y * cell_size + cell_size), 7)

def draw_grid():
    """Draw the Sudoku grid along with the default numbers."""
    for i in range(grid_size):
        for j in range(grid_size):
            if default_grid[i][j] != 0:
                pygame.draw.rect(window, (255, 255, 0), (i * cell_size, j * cell_size, cell_size + 1, cell_size + 1))
                text = font_large.render(str(default_grid[i][j]), 1, (0, 0, 0))
                window.blit(text, (i * cell_size + 15, j * cell_size + 15))
    
    for i in range(grid_size + 1):
        thickness = 7 if i % 3 == 0 else 1
        pygame.draw.line(window, (0, 0, 0), (0, i * cell_size), (window_size, i * cell_size), thickness)
        pygame.draw.line(window, (0, 0, 0), (i * cell_size, 0), (i * cell_size, window_size), thickness)

def fill_cell_value(value):
    """Fill the selected cell with the current value."""
    text = font_large.render(str(value), 1, (0, 0, 0))
    window.blit(text, (selected_x * cell_size + 15, selected_y * cell_size + 15))

def show_error_message(message):
    """Display an error message."""
    text = font_large.render(message, 1, (0, 0, 0))
    window.blit(text, (20, 570))

def is_valid_move(grid, row, col, num):
    """Check if it's valid to place the number in the cell."""
    for i in range(grid_size):
        if grid[row][i] == num or grid[i][col] == num:
            return False

    start_row, start_col = row // 3 * 3, col // 3 * 3
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True

def solve_sudoku(grid, row, col):
    """Solve the Sudoku puzzle using backtracking."""
    while grid[row][col] != 0:
        if row < grid_size - 1:
            row += 1
        elif row == grid_size - 1 and col < grid_size - 1:
            row = 0
            col += 1
        elif row == grid_size - 1 and col == grid_size - 1:
            return True

    pygame.event.pump()
    for num in range(1, grid_size + 1):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            global selected_x, selected_y
            selected_x, selected_y = row, col
            window.fill((255, 255, 255))
            draw_grid()
            highlight_selected_cell()
            pygame.display.update()
            pygame.time.delay(20)
            if solve_sudoku(grid, row, col):
                return True
            else:
                grid[row][col] = 0
            window.fill((0, 0, 0))
            draw_grid()
            highlight_selected_cell()
            pygame.display.update()
            pygame.time.delay(50)

    return False

def display_game_result():
    """Display the game finished message."""
    text = font_large.render("Game finished", 1, (0, 0, 0))
    window.blit(text, (20, 570))

# Game flags
running = True
cell_selected = False
solve_triggered = False
reset_triggered = False
display_error = False

# Game loop
while running:
    window.fill((173, 216, 230))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            cell_selected = True
            pos = pygame.mouse.get_pos()
            get_cell_coords(pos)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                selected_x = max(0, selected_x - 1)
                cell_selected = True
            if event.key == pygame.K_RIGHT:
                selected_x = min(grid_size - 1, selected_x + 1)
                cell_selected = True
            if event.key == pygame.K_UP:
                selected_y = max(0, selected_y - 1)
                cell_selected = True
            if event.key == pygame.K_DOWN:
                selected_y = min(grid_size - 1, selected_y + 1)
                cell_selected = True

            if event.key == pygame.K_1:
                current_value = 1
            if event.key == pygame.K_2:
                current_value = 2
            if event.key == pygame.K_3:
                current_value = 3
            if event.key == pygame.K_4:
                current_value = 4
            if event.key == pygame.K_5:
                current_value = 5
            if event.key == pygame.K_6:
                current_value = 6
            if event.key == pygame.K_7:
                current_value = 7
            if event.key == pygame.K_8:
                current_value = 8
            if event.key == pygame.K_9:
                current_value = 9
            
            if event.key == pygame.K_RETURN:
                solve_triggered = True
            
            if event.key == pygame.K_r:
                reset_triggered = True
                default_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
            
            if event.key == pygame.K_d:
                reset_triggered = True
                default_grid = [
                    [0, 0, 4, 0, 6, 0, 0, 0, 5],
                    [7, 8, 0, 4, 0, 0, 0, 2, 0],
                    [0, 0, 2, 6, 0, 1, 0, 7, 8],
                    [6, 1, 0, 0, 7, 5, 0, 0, 9],
                    [0, 0, 7, 5, 4, 0, 0, 6, 1],
                    [0, 0, 1, 7, 5, 0, 9, 3, 0],
                    [0, 7, 0, 3, 0, 0, 0, 1, 0],
                    [0, 4, 0, 2, 0, 6, 0, 0, 7],
                    [0, 2, 0, 0, 0, 7, 4, 0, 0],
                ]
    
    if solve_triggered:
        if not solve_sudoku(default_grid, 0, 0):
            display_error = True
        else:
            reset_triggered = True
        solve_triggered = False
    
    if current_value != 0:
        if default_grid[selected_x][selected_y] == 0:
            fill_cell_value(current_value)
            if is_valid_move(default_grid, selected_x, selected_y, current_value):
                default_grid[selected_x][selected_y] = current_value
                cell_selected = False
            else:
                default_grid[selected_x][selected_y] = 0
                show_error_message("Invalid move")
        current_value = 0
    
    if display_error:
        show_error_message("Solve Error")
    
    if reset_triggered:
        display_game_result()
    
    draw_grid()
    if cell_selected:
        highlight_selected_cell()
    
    pygame.display.update()

pygame.quit()