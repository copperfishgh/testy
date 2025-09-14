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
- Tactical helper system (visual board annotations)
- Strategic helper system (text analysis under board)
- Real-time position analysis engine

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

## Analysis System Design

Testy separates chess analysis into two distinct helper categories with **granular user control**:

### Helper Selection Interface
**Checkbox panel to the right of the chess board:**
- Individual checkboxes for each tactical and strategic helper
- Only checked helpers are active in analysis
- Settings persist across program sessions (saved to config file)
- Allows progressive learning and customized experience

**UI Layout:**
```
┌─────────────────┬─────────────────────┐
│                 │ TACTICAL HELPERS    │
│                 │ ☑ Hanging Pieces    │
│                 │ ☐ Immediate Threats │
│   CHESS BOARD   │ ☐ Simple Forks      │
│                 │ ☐ Pins & Skewers    │
│                 │ ☐ Material Wins     │
│                 │                     │
│                 │ STRATEGIC HELPERS   │
│                 │ ☐ Weak Pawns        │
│                 │ ☐ Open Files        │
│─────────────────│ ☐ Outpost Squares   │
│ [Flip Board]    │ ☐ Pawn Breaks       │
│                 │ ☐ Passed Pawns      │
│ Strategic Text: │                     │
│ • Analysis here │                     │
└─────────────────┴─────────────────────┘
```

### 🔴 Tactical Helpers (Default, Always Active)
**Visual annotations directly on the chess board:**
- **Hanging Pieces** - Red outlines around undefended pieces
- **Immediate Threats** - Warning symbols for mate in 1, checks
- **Simple Tactics** - Highlight forks, pins, skewers (1-2 move depth)
- **Material Wins** - Show squares where you can capture for free
- **Blunder Prevention** - Block moves that hang material

**Preview Analysis System:**
- **Current Position**: Shows tactical annotations for the current board state
- **Move Preview**: When piece selected and hovering over legal squares, shows "what if" analysis
- **Either/Or Display**: Shows current OR preview annotations, never both simultaneously
- **Real-time Feedback**: Instant tactical analysis when hovering over different legal moves
- **Performance Optimized**: Analysis only triggers on discrete square changes, not mouse movement

*Critical alerts that prevent immediate material loss or checkmate*

### 🔵 Strategic Helpers (Optional Checkbox)
**Text analysis panel under the board:**

**Pawn Structure Analysis:**
- **Weak Pawns** - Isolated, backward, doubled pawns
- **Pawn Breaks** - Suggest pawn advances like c5 to challenge center
- **Passed Pawns** - Identify advancement opportunities

**Positional Features:**
- **Open Files** - Available files for rook placement
- **Outpost Squares** - Strong squares protected by pawns, unreachable by enemy pawns
- **Piece Coordination** - Suggestions for better piece placement

**Example Strategic Output:**
```
Strategic Analysis:
• Backward pawn on d6 needs attention - consider c5 break
• Open g-file available for your rook
• Knight outpost available on e5 square
• Weak kingside pawn structure after h6
```

## Vision: The Perfect Chess Assistant

**Tactical Layer:** *"STOP! That hangs your queen!"* (Red board annotation)
**Strategic Layer:** *"Consider: Open d-file available"* (Blue text suggestion)

You make the strategic decisions. Testy prevents the tactical oversights and suggests positional improvements.

## Future: Rust Conversion

Once the Python version is complete, Testy will be converted to Rust for:
- Single executable distribution (~15MB)
- Better performance for real-time analysis
- Memory safety for chess engine calculations
- Learning modern systems programming

---

*A tool for chess players who want to improve their strategic thinking without worrying about hanging pieces.*