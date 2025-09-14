"""
Chess Display Module

This module handles the visual representation of the chess board and game state.
It provides functionality to display the board, pieces, and game information.
"""

from typing import Optional, Tuple, List
import pygame
from chess_board import BoardState, Piece, Color, PieceType

class ChessDisplay:
    """Handles the visual display of the chess game"""
    
    def __init__(self, window_width: int = 800, window_height: int = 600):
        """Initialize the display with window dimensions"""
        self.window_width = window_width
        self.window_height = window_height
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_SQUARE = (240, 217, 181)  # Light brown
        self.DARK_SQUARE = (181, 136, 99)    # Dark brown
        self.HIGHLIGHT = (255, 255, 0)       # Yellow for highlights
        self.SELECTED = (255, 0, 0)          # Red for selected square
        
        # Board dimensions (percentage-based)
        self.board_size = int(min(window_width, window_height * 0.9) * 0.85)  # 85% of smaller dimension, with 10% space for button
        self.square_size = self.board_size // 8
        
        # Position board with percentage-based margins
        self.board_offset_x = int(window_width * 0.07)  # 7% margin from left
        self.board_offset_y = int(window_height * 0.07)  # 7% margin from top
        
        # Ensure pygame is initialized before creating fonts
        if not pygame.get_init():
            pygame.init()
        
        # Font setup (percentage-based)
        self.font_large = pygame.font.Font(None, int(self.board_size * 0.09))   # 9% of board size
        self.font_medium = pygame.font.Font(None, int(self.board_size * 0.06))  # 6% of board size
        self.font_small = pygame.font.Font(None, int(self.board_size * 0.045))  # 4.5% of board size
        
        # Load piece images (placeholder - you'd load actual piece images here)
        self.piece_images = self._load_piece_images()

        # Create move indicator circle surface once
        self.move_indicator = self._create_move_indicator()

        # Checkmate animation variables
        self.checkmate_animation_start_time = None
        self.checkmate_king_position = None
    
    def _load_piece_images(self) -> dict:
        """Load and scale piece images from PNG files"""
        images = {}

        for color in [Color.WHITE, Color.BLACK]:
            for piece_type in PieceType:
                # Calculate piece size based on type (pawns smaller than other pieces)
                if piece_type == PieceType.PAWN:
                    piece_size = int(self.square_size * 0.65)
                else:
                    piece_size = int(self.square_size * 0.75)

                # Create filename based on naming convention: {color}{piece}.png
                color_prefix = "w" if color == Color.WHITE else "b"
                filename = f"pngs/2x/{color_prefix}{piece_type.value}.png"

                try:
                    # Load the original image
                    original_image = pygame.image.load(filename)

                    # Scale once using smooth scaling and cache it
                    scaled_image = pygame.transform.smoothscale(original_image, (piece_size, piece_size))

                    # Store with the key format used elsewhere in the code
                    key = f"{color.value}{piece_type.value}"
                    images[key] = scaled_image

                except pygame.error as e:
                    print(f"Warning: Could not load {filename}: {e}")
                    # Create a fallback colored rectangle if image loading fails
                    surface = pygame.Surface((piece_size, piece_size))
                    if color == Color.WHITE:
                        surface.fill(self.WHITE)
                    else:
                        surface.fill(self.BLACK)
                    pygame.draw.rect(surface, (100, 100, 100), surface.get_rect(), 2)

                    key = f"{color.value}{piece_type.value}"
                    images[key] = surface

        return images

    def _create_move_indicator(self) -> pygame.Surface:
        """Create a translucent circle surface for move indicators"""
        # Create a surface with per-pixel alpha
        circle_surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)

        # Circle size is 1/4 of the square
        circle_radius = self.square_size // 4
        center_x = self.square_size // 2
        center_y = self.square_size // 2

        # Draw translucent circle (green with 128 alpha for 50% transparency)
        circle_color = (0, 128, 0, 128)  # Green with 50% transparency
        pygame.draw.circle(circle_surface, circle_color, (center_x, center_y), circle_radius)

        return circle_surface

    def draw_move_indicator(self, screen, x: int, y: int) -> None:
        """Draw the pre-created move indicator at specified position"""
        screen.blit(self.move_indicator, (x, y))

    def start_checkmate_animation(self, board_state: BoardState) -> None:
        """Start the checkmate animation for the losing king"""
        import time
        self.checkmate_animation_start_time = time.time()

        # Find the checkmated king position
        losing_color = board_state.current_turn
        self.checkmate_king_position = board_state.get_king_position(losing_color)

    def draw_rotating_king(self, screen, piece: Piece, x: int, y: int, elapsed_time: float) -> None:
        """Draw a king rotating on its head"""
        # Animation duration is 0.5 seconds for 360 degree rotation
        animation_duration = 0.5

        if elapsed_time > animation_duration:
            # Animation finished, draw normally but upside down
            angle = 180
        else:
            # Calculate rotation angle (0 to 180 degrees over 0.5 seconds)
            progress = elapsed_time / animation_duration
            angle = progress * 180

        # Get the original piece image
        key = f"{piece.color.value}{piece.type.value}"
        if key in self.piece_images:
            original_surface = self.piece_images[key]

            # Rotate the image
            rotated_surface = pygame.transform.rotate(original_surface, angle)

            # Center the rotated image in the square
            rotated_rect = rotated_surface.get_rect()
            center_x = x + self.square_size // 2
            center_y = y + self.square_size // 2
            rotated_rect.center = (center_x, center_y)

            screen.blit(rotated_surface, rotated_rect)
        else:
            # Fallback to text
            piece_text = str(piece)
            text_surface = self.font_large.render(piece_text, True, self.BLACK)
            text_rect = text_surface.get_rect(center=(x + self.square_size//2, y + self.square_size//2))
            screen.blit(text_surface, text_rect)

    def draw_board(self, screen, board_state: BoardState, selected_square: Optional[Tuple[int, int]] = None,
                   possible_moves: List[Tuple[int, int]] = None, flipped: bool = False) -> None:
        """Draw the chess board with pieces"""
        if possible_moves is None:
            possible_moves = []
        
        # Draw the board squares
        for row in range(8):
            for col in range(8):
                # Apply flipping transformation
                display_row = (7 - row) if flipped else row
                display_col = (7 - col) if flipped else col
                x = self.board_offset_x + display_col * self.square_size
                y = self.board_offset_y + display_row * self.square_size
                
                # Determine square color (use original coordinates for coloring)
                is_light = (row + col) % 2 == 0
                color = self.LIGHT_SQUARE if is_light else self.DARK_SQUARE

                # Highlight selected square only
                if selected_square and selected_square == (row, col):
                    color = self.SELECTED

                # Draw the square
                pygame.draw.rect(screen, color,
                               (x, y, self.square_size, self.square_size))

                # Draw piece if present
                piece = board_state.get_piece(row, col)
                if piece:
                    self.draw_piece(screen, piece, x, y, row, col)

                # Draw move indicator circle for possible moves
                if (row, col) in possible_moves:
                    self.draw_move_indicator(screen, x, y)
        
        # Draw board border (use actual board size based on squares)
        actual_board_size = self.square_size * 8
        border_rect = pygame.Rect(self.board_offset_x - 2, self.board_offset_y - 2,
                                actual_board_size + 4, actual_board_size + 4)
        pygame.draw.rect(screen, self.BLACK, border_rect, 2)
        
        # Draw coordinates
        self.draw_coordinates(screen, flipped)
    
    def draw_piece(self, screen, piece: Piece, x: int, y: int, board_row: int = -1, board_col: int = -1) -> None:
        """Draw a piece at the specified screen coordinates"""
        # Check if this is the checkmated king and animation is active
        if (self.checkmate_animation_start_time is not None and
            self.checkmate_king_position is not None and
            piece.type == PieceType.KING and
            (board_row, board_col) == self.checkmate_king_position):

            import time
            elapsed_time = time.time() - self.checkmate_animation_start_time
            self.draw_rotating_king(screen, piece, x, y, elapsed_time)
            return

        # Normal piece drawing
        key = f"{piece.color.value}{piece.type.value}"
        if key in self.piece_images:
            piece_surface = self.piece_images[key]
            # Center the piece in the square
            piece_x = x + (self.square_size - piece_surface.get_width()) // 2
            piece_y = y + (self.square_size - piece_surface.get_height()) // 2
            screen.blit(piece_surface, (piece_x, piece_y))
        else:
            # Fallback: draw piece as text
            piece_text = str(piece)
            text_surface = self.font_large.render(piece_text, True, self.BLACK)
            text_rect = text_surface.get_rect(center=(x + self.square_size//2, y + self.square_size//2))
            screen.blit(text_surface, text_rect)
    
    def draw_coordinates(self, screen, flipped: bool = False) -> None:
        """Draw board coordinates (a-h, 1-8)"""
        # Draw file letters (a-h)
        for col in range(8):
            letter = chr(ord('a') + (7 - col if flipped else col))
            x = self.board_offset_x + col * self.square_size + self.square_size // 2
            y = self.board_offset_y + self.board_size + 10
            
            text_surface = self.font_small.render(letter, True, self.BLACK)
            text_rect = text_surface.get_rect(center=(x, y))
            screen.blit(text_surface, text_rect)
        
        # Draw rank numbers (1-8)
        for row in range(8):
            number = str((row + 1) if flipped else (8 - row))
            x = self.board_offset_x - 20
            y = self.board_offset_y + row * self.square_size + self.square_size // 2
            
            text_surface = self.font_small.render(number, True, self.BLACK)
            text_rect = text_surface.get_rect(center=(x, y))
            screen.blit(text_surface, text_rect)
    
    def draw_game_info(self, screen, board_state: BoardState) -> None:
        """Draw game information panel"""
        # Position info panel to the right of the board with minimal spacing
        info_x = self.board_offset_x + self.board_size + 10
        info_y = self.board_offset_y
        line_height = 30
        
        # Current turn
        turn_text = f"Turn: {'White' if board_state.current_turn == Color.WHITE else 'Black'}"
        self.draw_text(screen, turn_text, info_x, info_y, self.font_medium)
        
        # Move number
        move_text = f"Move: {board_state.fullmove_number}"
        self.draw_text(screen, move_text, info_x, info_y + line_height, self.font_medium)
        
        # Halfmove clock (for 50-move rule)
        halfmove_text = f"Halfmove Clock: {board_state.halfmove_clock}"
        self.draw_text(screen, halfmove_text, info_x, info_y + line_height * 2, self.font_small)
        
        # Castling rights
        castling_y = info_y + line_height * 4
        self.draw_text(screen, "Castling Rights:", info_x, castling_y, self.font_medium)
        
        white_castling = []
        if board_state.castling_rights.white_kingside:
            white_castling.append("K")
        if board_state.castling_rights.white_queenside:
            white_castling.append("Q")
        
        black_castling = []
        if board_state.castling_rights.black_kingside:
            black_castling.append("k")
        if board_state.castling_rights.black_queenside:
            black_castling.append("q")
        
        castling_text = f"White: {''.join(white_castling) if white_castling else '-'}"
        self.draw_text(screen, castling_text, info_x, castling_y + 25, self.font_small)
        
        castling_text = f"Black: {''.join(black_castling) if black_castling else '-'}"
        self.draw_text(screen, castling_text, info_x, castling_y + 45, self.font_small)
        
        # En passant target
        if board_state.en_passant_target:
            ep_row, ep_col = board_state.en_passant_target
            ep_square = f"{chr(ord('a') + ep_col)}{8 - ep_row}"
            ep_text = f"En Passant: {ep_square}"
        else:
            ep_text = "En Passant: -"
        self.draw_text(screen, ep_text, info_x, castling_y + 80, self.font_small)
        
        # Game status
        status_y = castling_y + 120
        if board_state.checkmate_flag:
            status_text = "CHECKMATE!"
            status_color = (255, 0, 0)  # Red
        elif board_state.stalemate_flag:
            status_text = "STALEMATE"
            status_color = (255, 165, 0)  # Orange
        elif board_state.is_check:
            status_text = "CHECK"
            status_color = (255, 0, 0)  # Red
        else:
            status_text = "Game in Progress"
            status_color = (0, 128, 0)  # Green
        
        self.draw_text(screen, status_text, info_x, status_y, self.font_medium, status_color)
    
    def draw_text(self, screen, text: str, x: int, y: int, font: pygame.font.Font, 
                  color: Tuple[int, int, int] = None) -> None:
        """Draw text at the specified position"""
        if color is None:
            color = self.BLACK
        
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
    
    def get_square_from_mouse(self, mouse_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Convert mouse position to board square coordinates"""
        mouse_x, mouse_y = mouse_pos
        
        # Check if mouse is within board bounds
        if (self.board_offset_x <= mouse_x <= self.board_offset_x + self.board_size and
            self.board_offset_y <= mouse_y <= self.board_offset_y + self.board_size):
            
            col = (mouse_x - self.board_offset_x) // self.square_size
            row = (mouse_y - self.board_offset_y) // self.square_size
            
            if 0 <= row < 8 and 0 <= col < 8:
                return (row, col)
        
        return None
    
    def draw_move_history(self, screen, board_state: BoardState, max_moves: int = 10) -> None:
        """Draw recent move history"""
        history_x = self.board_offset_x
        history_y = self.board_offset_y + self.board_size + 10
        line_height = 20
        
        self.draw_text(screen, "Recent Moves:", history_x, history_y, self.font_medium)
        
        # Show last few moves
        recent_moves = board_state.move_history[-max_moves:]
        for i, move in enumerate(recent_moves):
            move_text = f"{i+1}. {move.notation}"
            self.draw_text(screen, move_text, history_x, history_y + 30 + i * line_height, self.font_small)
    
    def update_display(self, screen, board_state: BoardState, selected_square: Optional[Tuple[int, int]] = None,
                      possible_moves: List[Tuple[int, int]] = None, flipped: bool = False) -> None:
        """Update the entire display"""
        # Check for checkmate and start animation if needed
        if board_state.checkmate_flag and self.checkmate_animation_start_time is None:
            self.start_checkmate_animation(board_state)

        # Clear screen
        screen.fill(self.WHITE)

        # Draw all components
        self.draw_board(screen, board_state, selected_square, possible_moves, flipped)
        
        # Note: pygame.display.flip() is called in the main loop, not here
    
    def show_promotion_dialog(self, screen, color: Color) -> PieceType:
        """Show promotion dialog and return selected piece type"""
        # Define promotion pieces (Queen, Rook, Bishop, Knight)
        promotion_pieces = [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]

        # Dialog dimensions
        dialog_width = 400
        dialog_height = 150
        dialog_x = (self.window_width - dialog_width) // 2
        dialog_y = (self.window_height - dialog_height) // 2

        # Create semi-transparent overlay
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        screen.blit(overlay, (0, 0))

        # Draw dialog box
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(screen, self.WHITE, dialog_rect)
        pygame.draw.rect(screen, self.BLACK, dialog_rect, 3)

        # Draw title
        title_text = "Choose promotion piece:"
        title_surface = self.font_medium.render(title_text, True, self.BLACK)
        title_rect = title_surface.get_rect(center=(dialog_x + dialog_width//2, dialog_y + 30))
        screen.blit(title_surface, title_rect)

        # Draw piece options
        piece_size = 60
        piece_spacing = (dialog_width - 4 * piece_size) // 5
        piece_rects = []

        for i, piece_type in enumerate(promotion_pieces):
            piece_x = dialog_x + piece_spacing + i * (piece_size + piece_spacing)
            piece_y = dialog_y + 70
            piece_rect = pygame.Rect(piece_x, piece_y, piece_size, piece_size)
            piece_rects.append((piece_rect, piece_type))

            # Draw piece background
            pygame.draw.rect(screen, self.LIGHT_SQUARE, piece_rect)
            pygame.draw.rect(screen, self.BLACK, piece_rect, 2)

            # Draw piece image or text
            key = f"{color.value}{piece_type.value}"
            if key in self.piece_images:
                # Scale the piece image to fit
                piece_surface = pygame.transform.smoothscale(self.piece_images[key], (piece_size - 10, piece_size - 10))
                piece_x_centered = piece_x + (piece_size - piece_surface.get_width()) // 2
                piece_y_centered = piece_y + (piece_size - piece_surface.get_height()) // 2
                screen.blit(piece_surface, (piece_x_centered, piece_y_centered))
            else:
                # Fallback to text
                piece_text = piece_type.value
                text_surface = self.font_large.render(piece_text, True, self.BLACK)
                text_rect = text_surface.get_rect(center=piece_rect.center)
                screen.blit(text_surface, text_rect)

        pygame.display.flip()

        # Wait for user selection
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for piece_rect, piece_type in piece_rects:
                        if piece_rect.collidepoint(mouse_pos):
                            return piece_type
                elif event.type == pygame.KEYDOWN:
                    # Keyboard shortcuts
                    if event.key == pygame.K_q:
                        return PieceType.QUEEN
                    elif event.key == pygame.K_r:
                        return PieceType.ROOK
                    elif event.key == pygame.K_b:
                        return PieceType.BISHOP
                    elif event.key == pygame.K_n:
                        return PieceType.KNIGHT
                    elif event.key == pygame.K_ESCAPE:
                        return PieceType.QUEEN  # Default to queen

    def quit(self) -> None:
        """Clean up Pygame resources"""
        pygame.quit()

# Example usage
if __name__ == "__main__":
    from chess_board import BoardState
    
    # Initialize pygame and create screen
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Chess Game - Example")
    
    # Create display and board
    display = ChessDisplay(1000, 700)
    board = BoardState()
    
    # Simple display loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update display
        display.update_display(screen, board)
        pygame.display.flip()
        clock.tick(60)
    
    display.quit()
