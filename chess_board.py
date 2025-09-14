"""
Chess Board State Data Structure

This module defines a comprehensive chess board state that tracks:
- Current piece positions
- Castling rights (kingside/queenside for both colors)
- En passant target square
- Move history and counters
- Game state information (turn, check status, etc.)
"""

from typing import Optional, List, Tuple, Dict, Any
from enum import Enum
from dataclasses import dataclass, field
import copy

class PieceType(Enum):
    """Chess piece types"""
    PAWN = "P"
    ROOK = "R"
    KNIGHT = "N"
    BISHOP = "B"
    QUEEN = "Q"
    KING = "K"

class Color(Enum):
    """Chess piece colors"""
    WHITE = "w"
    BLACK = "b"

class GamePhase(Enum):
    """Game phases"""
    OPENING = "opening"
    MIDDLEGAME = "middlegame"
    ENDGAME = "endgame"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    DRAW = "draw"

@dataclass
class Piece:
    """Represents a chess piece"""
    type: PieceType
    color: Color
    has_moved: bool = False  # Important for castling and pawn double moves
    
    def __str__(self) -> str:
        """String representation: uppercase for white, lowercase for black"""
        symbol = self.type.value
        return symbol.upper() if self.color == Color.WHITE else symbol.lower()

@dataclass
class CastlingRights:
    """Tracks castling rights for both colors"""
    white_kingside: bool = True
    white_queenside: bool = True
    black_kingside: bool = True
    black_queenside: bool = True
    
    def can_castle(self, color: Color, kingside: bool) -> bool:
        """Check if a color can castle in a specific direction"""
        if color == Color.WHITE:
            return self.white_kingside if kingside else self.white_queenside
        else:
            return self.black_kingside if kingside else self.black_queenside
    
    def lose_castling_right(self, color: Color, kingside: bool) -> None:
        """Remove castling rights"""
        if color == Color.WHITE:
            if kingside:
                self.white_kingside = False
            else:
                self.white_queenside = False
        else:
            if kingside:
                self.black_kingside = False
            else:
                self.black_queenside = False
    
    def lose_all_castling_rights(self, color: Color) -> None:
        """Remove all castling rights for a color (when king moves)"""
        if color == Color.WHITE:
            self.white_kingside = False
            self.white_queenside = False
        else:
            self.black_kingside = False
            self.black_queenside = False

@dataclass
class Move:
    """Represents a chess move with all relevant information"""
    from_square: Tuple[int, int]  # (row, col)
    to_square: Tuple[int, int]    # (row, col)
    piece: Piece
    captured_piece: Optional[Piece] = None
    promotion: Optional[PieceType] = None
    is_castle: bool = False
    castle_kingside: bool = False
    is_en_passant: bool = False
    is_double_pawn_push: bool = False
    move_number: int = 0
    notation: str = ""  # Algebraic notation like "Nf3", "O-O", "exd5"
    
    def __str__(self) -> str:
        return self.notation if self.notation else f"{self.from_square} -> {self.to_square}"

@dataclass
class BoardState:
    """
    Comprehensive chess board state that tracks all game information
    """
    # Current board position (8x8 grid)
    board: List[List[Optional[Piece]]] = field(default_factory=lambda: [[None for _ in range(8)] for _ in range(8)])
    
    # Game state
    current_turn: Color = Color.WHITE
    move_number: int = 1
    halfmove_clock: int = 0  # For 50-move rule
    fullmove_number: int = 1
    
    # Castling rights
    castling_rights: CastlingRights = field(default_factory=CastlingRights)
    
    # En passant target square (None if no en passant possible)
    en_passant_target: Optional[Tuple[int, int]] = None
    
    # Game status
    is_check: bool = False
    is_checkmate: bool = False
    is_stalemate: bool = False
    game_phase: GamePhase = GamePhase.OPENING
    
    # Move history
    move_history: List[Move] = field(default_factory=list)
    
    # Position repetition tracking (for threefold repetition rule)
    position_history: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize the board with starting position"""
        if not any(any(row) for row in self.board):  # If board is empty
            self.setup_initial_position()
    
    def setup_initial_position(self) -> None:
        """Set up the standard chess starting position"""
        # Clear the board
        self.board = [[None for _ in range(8)] for _ in range(8)]
        
        # Place black pieces (rows 0-1)
        piece_order = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
                      PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK]
        
        # Black back rank
        for col, piece_type in enumerate(piece_order):
            self.board[0][col] = Piece(piece_type, Color.BLACK)
        
        # Black pawns
        for col in range(8):
            self.board[1][col] = Piece(PieceType.PAWN, Color.BLACK)
        
        # Place white pieces (rows 6-7)
        # White pawns
        for col in range(8):
            self.board[6][col] = Piece(PieceType.PAWN, Color.WHITE)
        
        # White back rank
        for col, piece_type in enumerate(piece_order):
            self.board[7][col] = Piece(piece_type, Color.WHITE)
    
    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Get piece at a specific position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def set_piece(self, row: int, col: int, piece: Optional[Piece]) -> None:
        """Set piece at a specific position"""
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece
    
    def get_king_position(self, color: Color) -> Optional[Tuple[int, int]]:
        """Find the king of a specific color"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.type == PieceType.KING and piece.color == color:
                    return (row, col)
        return None
    
    def is_square_attacked(self, row: int, col: int, by_color: Color) -> bool:
        """
        Check if a square is attacked by pieces of a specific color.
        This is a simplified version - in a full implementation, you'd check
        all piece movement patterns.
        """
        # This is a placeholder - full implementation would check all piece types
        # For now, just return False to avoid infinite complexity
        return False
    
    def is_king_in_check(self, color: Color) -> bool:
        """Check if the king of a specific color is in check"""
        king_pos = self.get_king_position(color)
        if not king_pos:
            return False
        return self.is_square_attacked(king_pos[0], king_pos[1], Color.BLACK if color == Color.WHITE else Color.WHITE)
    
    def can_castle(self, color: Color, kingside: bool) -> bool:
        """Check if castling is possible"""
        if not self.castling_rights.can_castle(color, kingside):
            return False
        
        if self.is_king_in_check(color):
            return False
        
        # Check if squares between king and rook are empty and not attacked
        king_row = 0 if color == Color.BLACK else 7
        if kingside:
            # Check squares f1/g1 for white, f8/g8 for black
            for col in [5, 6]:
                if self.board[king_row][col] is not None:
                    return False
                if self.is_square_attacked(king_row, col, Color.BLACK if color == Color.WHITE else Color.WHITE):
                    return False
        else:
            # Check squares b1/c1/d1 for white, b8/c8/d8 for black
            for col in [1, 2, 3]:
                if self.board[king_row][col] is not None:
                    return False
                if self.is_square_attacked(king_row, col, Color.BLACK if color == Color.WHITE else Color.WHITE):
                    return False
        
        return True
    
    def get_fen_position(self) -> str:
        """Generate FEN (Forsyth-Edwards Notation) string for the current position"""
        fen_parts = []
        
        # Board position
        for row in self.board:
            empty_count = 0
            row_str = ""
            for piece in row:
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        row_str += str(empty_count)
                        empty_count = 0
                    row_str += str(piece)
            if empty_count > 0:
                row_str += str(empty_count)
            fen_parts.append(row_str)
        
        board_fen = "/".join(fen_parts)
        
        # Active color
        active_color = "w" if self.current_turn == Color.WHITE else "b"
        
        # Castling rights
        castling = ""
        if self.castling_rights.white_kingside:
            castling += "K"
        if self.castling_rights.white_queenside:
            castling += "Q"
        if self.castling_rights.black_kingside:
            castling += "k"
        if self.castling_rights.black_queenside:
            castling += "q"
        if not castling:
            castling = "-"
        
        # En passant target
        if self.en_passant_target:
            col_letter = chr(ord('a') + self.en_passant_target[1])
            row_number = 8 - self.en_passant_target[0]
            ep_target = f"{col_letter}{row_number}"
        else:
            ep_target = "-"
        
        # Halfmove and fullmove clocks
        halfmove = str(self.halfmove_clock)
        fullmove = str(self.fullmove_number)
        
        return f"{board_fen} {active_color} {castling} {ep_target} {halfmove} {fullmove}"
    
    def copy(self) -> 'BoardState':
        """Create a deep copy of the board state"""
        return copy.deepcopy(self)
    
    def __str__(self) -> str:
        """String representation of the board"""
        result = "  a b c d e f g h\n"
        for row in range(8):
            result += f"{8-row} "
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    result += str(piece) + " "
                else:
                    result += ". "
            result += f"{8-row}\n"
        result += "  a b c d e f g h\n"
        return result

    def get_possible_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all possible moves for a piece at the given position"""
        piece = self.get_piece(row, col)
        if not piece:
            return []

        if piece.type == PieceType.PAWN:
            return self._get_pawn_moves(row, col, piece.color)
        elif piece.type == PieceType.ROOK:
            return self._get_rook_moves(row, col, piece.color)
        elif piece.type == PieceType.KNIGHT:
            return self._get_knight_moves(row, col, piece.color)
        elif piece.type == PieceType.BISHOP:
            return self._get_bishop_moves(row, col, piece.color)
        elif piece.type == PieceType.QUEEN:
            return self._get_queen_moves(row, col, piece.color)
        elif piece.type == PieceType.KING:
            return self._get_king_moves(row, col, piece.color)

        return []

    def _is_valid_square(self, row: int, col: int) -> bool:
        """Check if a square is within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8

    def _is_square_empty_or_enemy(self, row: int, col: int, color: Color) -> bool:
        """Check if a square is empty or contains an enemy piece"""
        if not self._is_valid_square(row, col):
            return False
        piece = self.get_piece(row, col)
        return piece is None or piece.color != color

    def _get_pawn_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get possible moves for a pawn"""
        moves = []
        direction = -1 if color == Color.WHITE else 1  # White moves up (-1), Black moves down (+1)
        start_row = 6 if color == Color.WHITE else 1

        # Forward move
        new_row = row + direction
        if self._is_valid_square(new_row, col) and self.get_piece(new_row, col) is None:
            moves.append((new_row, col))

            # Double forward move from starting position
            if row == start_row:
                new_row = row + 2 * direction
                if self._is_valid_square(new_row, col) and self.get_piece(new_row, col) is None:
                    moves.append((new_row, col))

        # Diagonal captures
        for dc in [-1, 1]:
            new_row, new_col = row + direction, col + dc
            if self._is_valid_square(new_row, new_col):
                piece = self.get_piece(new_row, new_col)
                if piece and piece.color != color:
                    moves.append((new_row, new_col))

        # En passant capture
        if self.en_passant_target:
            ep_row, ep_col = self.en_passant_target
            if row + direction == ep_row and abs(col - ep_col) == 1:
                moves.append((ep_row, ep_col))

        return moves

    def _get_rook_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get possible moves for a rook"""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up

        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * dr, col + i * dc
                if not self._is_valid_square(new_row, new_col):
                    break

                piece = self.get_piece(new_row, new_col)
                if piece is None:
                    moves.append((new_row, new_col))
                elif piece.color != color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves

    def _get_knight_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get possible moves for a knight"""
        moves = []
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if self._is_square_empty_or_enemy(new_row, new_col, color):
                moves.append((new_row, new_col))

        return moves

    def _get_bishop_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get possible moves for a bishop"""
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonal directions

        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * dr, col + i * dc
                if not self._is_valid_square(new_row, new_col):
                    break

                piece = self.get_piece(new_row, new_col)
                if piece is None:
                    moves.append((new_row, new_col))
                elif piece.color != color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves

    def _get_queen_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get possible moves for a queen (combination of rook and bishop)"""
        return self._get_rook_moves(row, col, color) + self._get_bishop_moves(row, col, color)

    def _get_king_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get possible moves for a king"""
        moves = []
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in king_moves:
            new_row, new_col = row + dr, col + dc
            if self._is_square_empty_or_enemy(new_row, new_col, color):
                moves.append((new_row, new_col))

        # TODO: Add castling logic here

        return moves

    def make_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Execute a move if it's legal. Returns True if move was successful."""
        # Validate the move is in the list of possible moves
        possible_moves = self.get_possible_moves(from_row, from_col)
        if (to_row, to_col) not in possible_moves:
            return False

        # Get the piece to move
        piece = self.get_piece(from_row, from_col)
        if not piece:
            return False

        # Verify it's the correct player's turn
        if piece.color != self.current_turn:
            return False

        # Store captured piece for move history
        captured_piece = self.get_piece(to_row, to_col)

        # Execute the move
        self.set_piece(to_row, to_col, piece)
        self.set_piece(from_row, from_col, None)

        # Mark piece as moved (important for castling and pawn double moves)
        piece.has_moved = True

        # Handle special pawn moves
        if piece.type == PieceType.PAWN:
            # Check for double move to set en passant target
            if abs(to_row - from_row) == 2:
                self.en_passant_target = (from_row + (to_row - from_row) // 2, to_col)
            else:
                self.en_passant_target = None

            # Handle en passant capture
            if captured_piece is None and abs(to_col - from_col) == 1:
                # This is an en passant capture, remove the captured pawn
                captured_pawn_row = from_row
                self.set_piece(captured_pawn_row, to_col, None)
        else:
            self.en_passant_target = None

        # Update move counters
        if captured_piece or piece.type == PieceType.PAWN:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # Switch turns
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE

        if self.current_turn == Color.WHITE:
            self.fullmove_number += 1

        # Create and store move in history
        move = Move(
            from_square=(from_row, from_col),
            to_square=(to_row, to_col),
            piece=piece,
            captured_piece=captured_piece,
            move_number=self.fullmove_number
        )
        self.move_history.append(move)

        return True

# Example usage and testing
if __name__ == "__main__":
    # Create a new board state
    board = BoardState()
    
    print("Initial Chess Position:")
    print(board)
    print(f"FEN: {board.get_fen_position()}")
    print(f"Current turn: {board.current_turn.value}")
    print(f"Castling rights - White: K={board.castling_rights.white_kingside}, Q={board.castling_rights.white_queenside}")
    print(f"Castling rights - Black: k={board.castling_rights.black_kingside}, q={board.castling_rights.black_queenside}")
    print(f"En passant target: {board.en_passant_target}")
    print(f"Halfmove clock: {board.halfmove_clock}")
    print(f"Fullmove number: {board.fullmove_number}")
