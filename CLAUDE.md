# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Blundex is a Python chess tactical analysis application built with Pygame. It's designed as a real-time chess analysis tool that helps players avoid blunders and tactical oversights while focusing on strategic play. The project follows a modular architecture with clear separation between chess logic, display, and configuration.

## Running the Application

```bash
python main.py
```

The application requires Python 3.x with Pygame. Optional dependencies include NumPy for sound generation.

## Architecture

### Core Module Structure

**main.py** - Application entry point and main game loop
- Initializes Pygame and creates the main window
- Handles all user input (keyboard shortcuts, mouse events)
- Manages drag-and-drop piece movement system
- Controls animation timing and rendering optimization

**chess_board.py** - Complete chess game logic and state management
- `BoardState` class: Comprehensive chess position tracking
- Full chess rules implementation including castling, en passant, pawn promotion
- Legal move generation with check validation
- Undo/redo system with 50-move history limit
- Caching system for hanging pieces and exchange evaluation
- FEN notation support for position representation

**display.py** - Visual rendering and user interface
- `ChessDisplay` class: All graphical output and UI components
- Board rendering with coordinate system and piece positioning
- Helper panel with configurable tactical assistance options
- Drag-and-drop visual feedback and move preview system
- Animation system for checkmate/stalemate effects
- Settings persistence using JSON configuration files

**config.py** - Configuration constants and settings
- `GameConfig`: Window sizing and layout percentages
- `Colors`: Complete color scheme for board and UI elements
- `AudioConfig`: Sound system configuration
- `GameConstants`: Chess piece values and game constants

**sound_manager.py** - Audio system management
- Sound generation using NumPy or system fallbacks
- Error sound feedback for invalid moves
- Cross-platform audio support with graceful degradation

### Key Design Patterns

**Modular Architecture**: Clear separation between game logic, display, and configuration
**Caching System**: Performance optimization for tactical analysis (hanging pieces, exchange evaluation)
**Event-Driven Input**: Comprehensive keyboard shortcuts and mouse interaction system
**Settings Persistence**: User preferences saved to `.blundex` configuration file
**Graceful Degradation**: Fallbacks for missing dependencies (NumPy, audio system)

### Asset Management

The `pngs/2x/` directory contains chess piece images in the format `{color}{piece}.png`:
- Colors: `w` (white), `b` (black)
- Pieces: `P` (pawn), `R` (rook), `N` (knight), `B` (bishop), `Q` (queen), `K` (king)
- Example: `wK.png` (white king), `bQ.png` (black queen)

### Game Controls

- **F** - Flip board perspective
- **U/R** - Undo/Redo moves
- **H** - Toggle hanging pieces helper
- **E** - Toggle exchange evaluation helper
- **~** - Reset game to starting position
- **/** - Show/hide keyboard shortcuts panel
- **ESC** - Exit application

### Tactical Helper System

The application features a checkbox-based helper system:
- **Hanging Pieces**: Visual indicators for undefended pieces
- **Exchange Evaluation**: Tactical analysis with hover-based investigation
- Settings are persisted between sessions in `.blundex` file
- Helpers use cached computation for performance optimization

### Development Notes

- No build system or dependency management files (requirements.txt, etc.)
- Direct Python execution with standard library + Pygame
- Cross-platform Windows/Linux/macOS compatibility
- Memory-efficient with move history limits and caching systems
- Optimized rendering with smart redraw detection

### Future Architecture

The codebase is designed for eventual conversion to Rust for:
- Single executable distribution
- Improved performance for real-time analysis
- Memory safety for chess engine calculations
- Cross-platform deployment optimization