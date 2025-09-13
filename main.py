import pygame
import sys
from chess_board import BoardState
from display import ChessDisplay

# Initialize Pygame
pygame.init()

# Get screen dimensions
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# Calculate window size as percentage of screen (75%)
WINDOW_WIDTH = int(min(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.75))  # 75% of smaller dimension
WINDOW_HEIGHT = int(WINDOW_WIDTH * 1.1)  # Slightly taller for button

# Create display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chess Game")

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER = (150, 150, 150)
BUTTON_TEXT = (255, 255, 255)

# Create global chess board in starting position
chess_board = BoardState()

# Create display object
display = ChessDisplay(WINDOW_WIDTH, WINDOW_HEIGHT)

# Button properties (percentage-based)
button_width = int(WINDOW_WIDTH * 0.35)  # 35% of window width
button_height = int(WINDOW_HEIGHT * 0.08)  # 8% of window height
button_x = (WINDOW_WIDTH - button_width) // 2  # Centered horizontally
button_y = int(WINDOW_HEIGHT * 0.9)  # 90% down from top
flip_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# Font setup (percentage-based)
font_size = int(WINDOW_WIDTH * 0.05)  # 5% of window width
font = pygame.font.Font(None, font_size)

# Game state
board_flipped = False
selected_square = None
possible_moves = []

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_f:  # F key to flip board
                board_flipped = not board_flipped
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if flip button was clicked
            if flip_button_rect.collidepoint(mouse_pos):
                board_flipped = not board_flipped
            else:
                # Handle board clicks for piece selection/movement
                square = display.get_square_from_mouse(mouse_pos)
                if square:
                    # Convert square coordinates if board is flipped
                    if board_flipped:
                        square = (7 - square[0], 7 - square[1])
                    
                    if selected_square is None:
                        # Select a piece
                        piece = chess_board.get_piece(square[0], square[1])
                        if piece and piece.color == chess_board.current_turn:
                            selected_square = square
                            # TODO: Calculate possible moves for the selected piece
                            possible_moves = []  # Placeholder
                    else:
                        # Try to move the piece
                        if square in possible_moves:
                            # TODO: Implement actual move logic
                            print(f"Move from {selected_square} to {square}")
                            selected_square = None
                            possible_moves = []
                        elif square == selected_square:
                            # Deselect
                            selected_square = None
                            possible_moves = []
                        else:
                            # Select different piece
                            piece = chess_board.get_piece(square[0], square[1])
                            if piece and piece.color == chess_board.current_turn:
                                selected_square = square
                                possible_moves = []
    
    # Draw the chess board (with flip consideration)
    display.update_display(screen, chess_board, selected_square, possible_moves, board_flipped)
    
    # Draw flip button
    button_color = BUTTON_HOVER if flip_button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, flip_button_rect)
    pygame.draw.rect(screen, BLACK, flip_button_rect, 2)  # Border
    
    # Draw button text
    button_text = "Flip Board" if not board_flipped else "Unflip Board"
    text_surface = font.render(button_text, True, BUTTON_TEXT)
    text_rect = text_surface.get_rect(center=flip_button_rect.center)
    screen.blit(text_surface, text_rect)
    
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
