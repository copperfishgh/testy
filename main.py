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
RGB_WHITE = (255, 255, 255)
RGB_BLACK = (0, 0, 0)
BUTTON_BACKGROUND_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Initialize mixer for sounds
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

def play_error_beep():
    """Play system error beep sound"""
    import winsound
    # Play system beep (frequency 800Hz, duration 300ms)
    winsound.Beep(800, 300)

# Check if we can create pygame sounds (requires NumPy)
def create_error_sound():
    """Create a simple error beep sound using pygame"""
    try:
        import numpy as np
        sample_rate = 22050
        duration = 0.3  # 300ms
        frequency = 800  # 800Hz beep

        # Generate beep sound
        frames = int(duration * sample_rate)
        arr = np.zeros(frames)

        for i in range(frames):
            # Fade in/out to avoid clicks
            fade_frames = int(0.01 * sample_rate)  # 10ms fade
            if i < fade_frames:
                fade = i / fade_frames
            elif i > frames - fade_frames:
                fade = (frames - i) / fade_frames
            else:
                fade = 1.0

            arr[i] = fade * np.sin(2 * np.pi * frequency * i / sample_rate)

        # Convert to 16-bit integers
        arr = (arr * 32767).astype(np.int16)

        # Create stereo array
        stereo_arr = np.zeros((frames, 2), dtype=np.int16)
        stereo_arr[:, 0] = arr
        stereo_arr[:, 1] = arr

        return pygame.sndarray.make_sound(stereo_arr)
    except ImportError:
        return None

# Try to create pygame sound, fallback to system beep
try:
    error_sound = create_error_sound()
    if error_sound:
        print("Pygame error sound created successfully")
    else:
        print("Using system beep for error sound")
except Exception as e:
    print(f"Could not create pygame sound, using system beep: {e}")
    error_sound = None

# Create global board state in starting position
board_state = BoardState()

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
is_board_flipped = False
selected_square_coords = None
highlighted_moves = []

# Main game loop
is_running = True
clock = pygame.time.Clock()

while is_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
            elif event.key == pygame.K_f:  # F key to flip board
                is_board_flipped = not is_board_flipped
            elif event.key == pygame.K_u:  # U key to undo
                if board_state.can_undo():
                    success = board_state.undo_move()
                    if success:
                        print("Move undone")
                        # Clear any current selection
                        selected_square_coords = None
                        highlighted_moves = []
                    else:
                        print("Undo failed")
                        if error_sound:
                            error_sound.play()
                        else:
                            play_error_beep()
                else:
                    print("Nothing to undo")
                    if error_sound:
                        error_sound.play()
                    else:
                        play_error_beep()
            elif event.key == pygame.K_r:  # R key to redo
                if board_state.can_redo():
                    success = board_state.redo_move()
                    if success:
                        print("Move redone")
                        # Clear any current selection
                        selected_square_coords = None
                        highlighted_moves = []
                    else:
                        print("Redo failed")
                        if error_sound:
                            error_sound.play()
                        else:
                            play_error_beep()
                else:
                    print("Nothing to redo")
                    if error_sound:
                        error_sound.play()
                    else:
                        play_error_beep()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if flip button was clicked
            if flip_button_rect.collidepoint(mouse_pos):
                is_board_flipped = not is_board_flipped
            else:
                # Handle board clicks for piece selection/movement
                square = display.get_square_from_mouse(mouse_pos)
                if square:
                    # Convert square coordinates if board is flipped
                    if is_board_flipped:
                        square = (7 - square[0], 7 - square[1])
                    
                    if selected_square_coords is None:
                        # Select a piece
                        piece = board_state.get_piece(square[0], square[1])
                        if piece and piece.color == board_state.current_turn:
                            selected_square_coords = square
                            # Calculate possible moves for the selected piece
                            highlighted_moves = board_state.get_possible_moves(square[0], square[1])
                    else:
                        # Try to move the piece
                        if square in highlighted_moves:
                            # Check if this is a pawn promotion
                            if board_state.is_pawn_promotion(selected_square_coords[0], selected_square_coords[1], square[0], square[1]):
                                # Show promotion dialog
                                current_piece = board_state.get_piece(selected_square_coords[0], selected_square_coords[1])
                                promotion_piece = display.show_promotion_dialog(screen, current_piece.color)

                                # Execute the move with promotion
                                move_successful = board_state.make_move_with_promotion(
                                    selected_square_coords[0], selected_square_coords[1],
                                    square[0], square[1], promotion_piece
                                )
                                if move_successful:
                                    print(f"Promotion move from {selected_square_coords} to {square}, promoted to {promotion_piece.value}")
                                else:
                                    print("Promotion move failed!")
                            else:
                                # Execute regular move
                                move_successful = board_state.make_move(
                                    selected_square_coords[0], selected_square_coords[1],
                                    square[0], square[1]
                                )
                                if move_successful:
                                    print(f"Move from {selected_square_coords} to {square}")
                                else:
                                    print("Move failed!")  # This shouldn't happen if move validation works

                            # Clear selection regardless
                            selected_square_coords = None
                            highlighted_moves = []
                        elif square == selected_square_coords:
                            # Deselect
                            selected_square_coords = None
                            highlighted_moves = []
                        else:
                            # Select different piece
                            piece = board_state.get_piece(square[0], square[1])
                            if piece and piece.color == board_state.current_turn:
                                selected_square_coords = square
                                highlighted_moves = board_state.get_possible_moves(square[0], square[1])
    
    # Draw the chess board (with flip consideration)
    display.update_display(screen, board_state, selected_square_coords, highlighted_moves, is_board_flipped)
    
    # Draw flip button
    button_color = BUTTON_HOVER_COLOR if flip_button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_BACKGROUND_COLOR
    pygame.draw.rect(screen, button_color, flip_button_rect)
    pygame.draw.rect(screen, RGB_BLACK, flip_button_rect, 2)  # Border
    
    # Draw button text
    button_text = "Flip Board" if not is_board_flipped else "Unflip Board"
    text_surface = font.render(button_text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=flip_button_rect.center)
    screen.blit(text_surface, text_rect)
    
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
