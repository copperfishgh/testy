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
        
        # Board dimensions - use a fixed size for now to debug
        self.board_size = 400  # Fixed size for debugging
        self.square_size = self.board_size // 8
        
        # Center the board in the window
        self.board_offset_x = (window_width - self.board_size) // 2
        self.board_offset_y = (window_height - self.board_size) // 2
        
        # Ensure pygame is initialized before creating fonts
        if not pygame.get_init():
            pygame.init()
        
        # Font setup
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Load piece images (placeholder - you'd load actual piece images here)
        self.piece_images = self._load_piece_images()
    
    def _load_piece_images(self) -> dict:
        """Load piece images - placeholder implementation"""
        # In a real implementation, you'd load actual piece images
        # For now, we'll create simple colored rectangles as placeholders
        images = {}
        
        for color in [Color.WHITE, Color.BLACK]:
            for piece_type in PieceType:
                key = f"{color.value}{piece_type.value}"
                # Create a simple colored square as placeholder
                surface = pygame.Surface((self.square_size - 10, self.square_size - 10))
                if color == Color.WHITE:
                    surface.fill(self.WHITE)
                else:
                    surface.fill(self.BLACK)
                pygame.draw.rect(surface, (100, 100, 100), surface.get_rect(), 2)
                images[key] = surface
        
        return images
    
    def draw_board(self, screen, board_state: BoardState, selected_square: Optional[Tuple[int, int]] = None, 
                   possible_moves: List[Tuple[int, int]] = None) -> None:
        """Draw the chess board with pieces"""
        if possible_moves is None:
            possible_moves = []
        
        # Draw the board squares
        for row in range(8):
            for col in range(8):
                x = self.board_offset_x + col * self.square_size
                y = self.board_offset_y + row * self.square_size
                
                # Determine square color
                is_light = (row + col) % 2 == 0
                color = self.LIGHT_SQUARE if is_light else self.DARK_SQUARE
                
                # Highlight selected square
                if selected_square and selected_square == (row, col):
                    color = self.SELECTED
                # Highlight possible moves
                elif (row, col) in possible_moves:
                    color = self.HIGHLIGHT
                
                # Draw the square
                pygame.draw.rect(screen, color, 
                               (x, y, self.square_size, self.square_size))
                
                # Draw piece if present
                piece = board_state.get_piece(row, col)
                if piece:
                    self.draw_piece(screen, piece, x, y)
        
        # Draw board border
        border_rect = pygame.Rect(self.board_offset_x - 2, self.board_offset_y - 2,
                                self.board_size + 4, self.board_size + 4)
        pygame.draw.rect(screen, self.BLACK, border_rect, 2)
        
        # Draw coordinates
        self.draw_coordinates(screen)
    
    def draw_piece(self, screen, piece: Piece, x: int, y: int) -> None:
        """Draw a piece at the specified screen coordinates"""
        # Get piece image
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
    
    def draw_coordinates(self, screen) -> None:
        """Draw board coordinates (a-h, 1-8)"""
        # Draw file letters (a-h)
        for col in range(8):
            letter = chr(ord('a') + col)
            x = self.board_offset_x + col * self.square_size + self.square_size // 2
            y = self.board_offset_y + self.board_size + 10
            
            text_surface = self.font_small.render(letter, True, self.BLACK)
            text_rect = text_surface.get_rect(center=(x, y))
            screen.blit(text_surface, text_rect)
        
        # Draw rank numbers (1-8)
        for row in range(8):
            number = str(8 - row)
            x = self.board_offset_x - 20
            y = self.board_offset_y + row * self.square_size + self.square_size // 2
            
            text_surface = self.font_small.render(number, True, self.BLACK)
            text_rect = text_surface.get_rect(center=(x, y))
            screen.blit(text_surface, text_rect)
    
    def draw_game_info(self, screen, board_state: BoardState) -> None:
        """Draw game information panel"""
        # Position info panel to the right of the board, but ensure it fits in window
        info_x = min(self.board_offset_x + self.board_size + 20, self.window_width - 180)
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
        if board_state.is_checkmate:
            status_text = "CHECKMATE!"
            status_color = (255, 0, 0)  # Red
        elif board_state.is_stalemate:
            status_text = "STALEMATE"
            status_color = (255, 165, 0)  # Orange
        elif board_state.is_check:
            status_text = "CHECK"
            status_color = (255, 0, 0)  # Red
        else:
            status_text = "Game in Progress"
            status_color = (0, 128, 0)  # Green
        
        self.draw_text(screen, status_text, info_x, status_y, self.font_medium, status_color)
        
        # FEN position (abbreviated)
        fen_text = board_state.get_fen_position()
        if len(fen_text) > 40:
            fen_text = fen_text[:40] + "..."
        self.draw_text(screen, "FEN:", info_x, status_y + 40, self.font_small)
        self.draw_text(screen, fen_text, info_x, status_y + 60, self.font_small)
    
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
        history_y = min(self.board_offset_y + self.board_size + 50, self.window_height - 100)
        line_height = 20
        
        self.draw_text(screen, "Recent Moves:", history_x, history_y, self.font_medium)
        
        # Show last few moves
        recent_moves = board_state.move_history[-max_moves:]
        for i, move in enumerate(recent_moves):
            move_text = f"{i+1}. {move.notation}"
            self.draw_text(screen, move_text, history_x, history_y + 30 + i * line_height, self.font_small)
    
    def update_display(self, screen, board_state: BoardState, selected_square: Optional[Tuple[int, int]] = None,
                      possible_moves: List[Tuple[int, int]] = None) -> None:
        """Update the entire display"""
        # Clear screen
        screen.fill(self.WHITE)
        
        # Draw all components
        self.draw_board(screen, board_state, selected_square, possible_moves)
        self.draw_game_info(screen, board_state)
        self.draw_move_history(screen, board_state)
        
        # Note: pygame.display.flip() is called in the main loop, not here
    
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
