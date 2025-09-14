# Testy - Chess Tactical Analysis Companion

**Testy** is a real-time chess analysis tool designed to catch blunders and tactical oversights while you focus on strategy. It's not a chess engine opponent or referee - it's your tactical safety net.

## What Testy Does

Testy watches your chess games and uses minimal lookahead analysis to:

- ✅ **Warn about blunders** - "That move hangs your queen"
- ✅ **Spot missed opportunities** - "You can win a rook with Rxd7"
- ✅ **Prevent basic mistakes** - "Your king will be in check"
- ✅ **Count material** - "Free pawn on e5"
- ✅ **Catch simple tactics** - Forks, pins, skewers in 1-2 moves

## What Testy Doesn't Do

- ❌ **Strategic evaluation** - No positional judgment or long-term planning
- ❌ **Deep calculation** - No extensive move tree searching
- ❌ **Play against you** - Not a chess opponent
- ❌ **Opening/endgame theory** - Focus is purely tactical

## The Philosophy

> *"Let me handle the strategy, you handle the blunders."*

Chess has two main components: **tactical accuracy** (not hanging pieces) and **strategic understanding** (planning, position evaluation). Most players want to develop their strategic thinking, but simple tactical oversights ruin games. Testy handles the tactical bookkeeping so you can focus on the strategic art of chess.

## Current Status

**Fully Functional Chess Interface:**
- Complete chess rule implementation with all special moves
- Visual board with piece movement and highlighting
- Undo/redo system for position exploration
- Pawn promotion, castling, en passant support
- Board flipping and responsive design
- Checkmate/stalemate detection with visual effects

**Still Needed for Full Testy Vision:**
- Blunder detection engine
- Tactical opportunity scanner
- Real-time alert system
- Basic tactical pattern recognition (pins, forks, skewers)

## Running Testy

```bash
python main.py
```

**Controls:**
- **Mouse** - Click to select and move pieces
- **F** - Flip board perspective
- **U** - Undo last move
- **R** - Redo move
- **ESC** - Quit

## Technical Details

- **Python 3.x** with Pygame for graphics
- **Modular architecture** - separate chess logic, display, and configuration
- **Responsive design** - scales to different screen sizes
- **FEN notation support** - standard position representation
- **Complete move validation** - ensures only legal moves are allowed

## Vision: The Perfect Chess Assistant

Imagine analyzing a position and having Testy quietly whisper:
- "Careful - that move hangs your bishop"
- "Rxd7 wins the exchange"
- "Check your back rank"
- "Free knight on f6"

You make the strategic decisions. Testy prevents the tactical oversights.

---

*A tool for chess players who want to improve their strategic thinking without worrying about hanging pieces.*