# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based chess game built with Pygame. The project implements a visual chess board with piece movement, board flipping, and comprehensive chess game state tracking.

## Architecture

### Core Components

- **`chess_board.py`**: Complete chess game state management
  - `BoardState` class: Tracks piece positions, turn order, castling rights, en passant, move history
  - `Piece` class: Represents individual chess pieces with type and color
  - Comprehensive data structures for chess rules (castling, en passant, move validation)
  - FEN notation support for position serialization

- **`display.py`**: Visual rendering and UI components
  - `ChessDisplay` class: Handles all pygame rendering
  - Responsive design using percentage-based positioning
  - Piece image loading system (currently uses placeholder rectangles)
  - Mouse-to-board coordinate conversion
  - Game information panel rendering

- **`main.py`**: Main game loop and event handling
  - Pygame initialization and window management
  - Mouse and keyboard event processing
  - Board flipping functionality (F key or button)
  - Piece selection and movement logic (partially implemented)

### Key Design Patterns

- **Separation of Concerns**: Game logic (`chess_board.py`) is separate from display (`display.py`) and main loop (`main.py`)
- **Data-Driven Design**: All game state is contained in `BoardState` class with immutable operations
- **Responsive UI**: All dimensions are percentage-based for different screen sizes

## Running the Application

```bash
python main.py
```

The application will create a window sized at 75% of screen dimensions and display a chess board in starting position.

## Development Commands

- Run the main application: `python main.py`
- Test PNG loading: `python testpng.py` (requires PNG files in `pngs/2x/` directory)
- Run individual modules: `python chess_board.py` or `python display.py` for their standalone examples

## Current Implementation Status

### Completed Features
- Complete chess board state tracking
- Visual board rendering with piece display
- Board coordinate system and mouse interaction
- Board flipping functionality
- Responsive window sizing
- Game state information display

### Incomplete Features
- **Move validation and execution**: Main game logic in `main.py` lines 84-102 has placeholder TODOs
- **Piece images**: Currently uses placeholder rectangles instead of actual piece graphics
- **Chess rule enforcement**: Move validation, check detection, and game end conditions need implementation
- **AI opponent**: No computer player implementation

## File Structure Notes

- `pngs/`: Directory for piece image assets (referenced in `testpng.py`)
- `graphics/`: Empty directory, likely intended for additional graphics assets
- `__pycache__/`: Python bytecode cache (gitignored)

## Important Implementation Details

- Board coordinates use (row, col) format where (0,0) is top-left (a8 in chess notation)
- Board flipping affects visual display but coordinate conversion happens in main loop
- Piece movement is event-driven through pygame mouse clicks
- The codebase is designed to support full chess rules but move validation is not yet implemented
- Font and image sizes scale with window dimensions for responsive design