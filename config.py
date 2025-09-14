"""
Configuration module for the Chess Game

This module contains all constants, settings, and configuration values
used throughout the application.
"""

class GameConfig:
    """Main game configuration settings"""

    # Window and display settings
    SCREEN_SIZE_PERCENTAGE = 0.75  # 75% of screen dimensions
    WINDOW_ASPECT_RATIO = 1.1      # Slightly taller for button
    BOARD_SIZE_PERCENTAGE = 0.85   # 85% of smaller window dimension
    BOARD_MARGIN_PERCENTAGE = 0.07 # 7% margin from edges

    # Button settings
    BUTTON_WIDTH_PERCENTAGE = 0.35  # 35% of window width
    BUTTON_HEIGHT_PERCENTAGE = 0.08 # 8% of window height
    BUTTON_Y_PERCENTAGE = 0.9       # 90% down from top

    # Font sizes (as percentage of board size)
    FONT_LARGE_PERCENTAGE = 0.09   # 9% of board size
    FONT_MEDIUM_PERCENTAGE = 0.06  # 6% of board size
    FONT_SMALL_PERCENTAGE = 0.045  # 4.5% of board size
    FONT_BUTTON_PERCENTAGE = 0.05  # 5% of window width

class Colors:
    """Color constants for the game"""

    # Basic RGB colors
    RGB_WHITE = (255, 255, 255)
    RGB_BLACK = (0, 0, 0)

    # Chess board colors
    LIGHT_SQUARE = (240, 217, 181)  # Light brown
    DARK_SQUARE = (181, 136, 99)    # Dark brown

    # UI highlight colors
    HIGHLIGHT = (255, 255, 0)       # Yellow for highlights
    SELECTED = (255, 0, 0)          # Red for selected square

    # Button colors
    BUTTON_BACKGROUND_COLOR = (100, 100, 100)
    BUTTON_HOVER_COLOR = (150, 150, 150)
    BUTTON_TEXT_COLOR = (255, 255, 255)

    # Text colors
    RED_TEXT = (255, 0, 0)
    BLACK_TEXT = (0, 0, 0)

    # Board annotation colors (neutral, warning, caution, positive)
    ANNOTATION_NEUTRAL = (128, 128, 128)     # Light grey for neutral/informational
    ANNOTATION_WARNING = (255, 0, 0)        # Red for strong warnings
    ANNOTATION_CAUTION = (255, 255, 0)      # Yellow for awareness/caution
    ANNOTATION_POSITIVE = (0, 255, 0)       # Green for good/positive

class AudioConfig:
    """Audio system configuration"""

    # Pygame mixer settings
    FREQUENCY = 22050
    SIZE = -16
    CHANNELS = 2
    BUFFER = 512

    # Error beep settings
    BEEP_FREQUENCY = 800   # 800Hz beep
    BEEP_DURATION = 300    # 300ms duration

    # Animation settings
    FADE_DURATION = 0.01   # 10ms fade in/out

class AnimationConfig:
    """Animation timing and settings"""

    # Checkmate animation
    CHECKMATE_ROTATION_DURATION = 0.5  # 0.5 seconds for king rotation
    CHECKMATE_FINAL_ANGLE = 180        # Final rotation angle (upside down)

    # Move animation
    MOVE_INDICATOR_RADIUS_FACTOR = 0.25  # Radius as factor of square size

class GameConstants:
    """Chess game constants"""

    BOARD_SIZE = 8
    UNDO_HISTORY_LIMIT = 50  # Maximum moves to keep for undo

    # File paths
    PIECE_IMAGE_DIRECTORY = "pngs/2x/"

    # Piece size factors
    PAWN_SIZE_FACTOR = 0.65     # Pawns are 65% of square size
    PIECE_SIZE_FACTOR = 0.75    # Other pieces are 75% of square size