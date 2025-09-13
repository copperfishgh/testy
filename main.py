import pygame
import sys
from chess_board import BoardState
from display import ChessDisplay

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
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

# Button properties
button_width = 150
button_height = 40
button_x = (WINDOW_WIDTH - button_width) // 2
button_y = WINDOW_HEIGHT - 60
flip_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# Font setup
font = pygame.font.Font(None, 24)

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
    # Note: display.update_display() handles screen clearing
    if board_flipped:
        # Create a flipped version of the board for display
        # This is a simplified approach - in a full implementation,
        # you'd want to modify the display logic to handle flipping
        display.update_display(screen, chess_board, selected_square, possible_moves)
    else:
        display.update_display(screen, chess_board, selected_square, possible_moves)
    
    # Draw flip button
    button_color = BUTTON_HOVER if flip_button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, flip_button_rect)
    pygame.draw.rect(screen, BLACK, flip_button_rect, 2)  # Border
    
    # Draw button text
    button_text = "Flip Board" if not board_flipped else "Unflip Board"
    text_surface = font.render(button_text, True, BUTTON_TEXT)
    text_rect = text_surface.get_rect(center=flip_button_rect.center)
    screen.blit(text_surface, text_rect)
    
    # Draw additional info
    info_text = f"Board Orientation: {'Flipped' if board_flipped else 'Normal'}"
    info_surface = font.render(info_text, True, BLACK)
    screen.blit(info_surface, (10, 10))
    
    # Draw instructions
    instructions = "Click pieces to select, F key or button to flip board"
    inst_surface = font.render(instructions, True, BLACK)
    screen.blit(inst_surface, (10, WINDOW_HEIGHT - 30))
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
