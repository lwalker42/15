<h1 align="center">15</h1>

<p align="center">Esoteric language inspired by the 15 sliding puzzle</p>

<p align="center">
<img width="60%" src="assets\15-puzzle.jpg">
</p>

<br/><br/>

## Usage
---
Run `python 15 filename.15` or `import 15/fifteen` to use the interpreter on it's own and step through execution.

<br/>

## Overview
---
The main goal of this language is to have the execution mimic the movement of 15 puzzle play.  To this end, each step of the program is analogous to moving a piece in the puzzle, and execution halts *if and only if* the puzzle is solved.
- The program has two parts: an instruction array, and the puzzle piece array
- Per the analogy, the commands are written on the backboard and then the pieces (`1` to `n`) are placed on top leaving a single empty space
- Every step, the revealed instruction in the empty space is executed and an piece is moved, thus revealing a new empty space for the next step
- Each of the pieces are also unbounded memory cells, and the empty space also acts as an accumulator.  These memory cells are initialized to the value of their respective pieces at the start of execution (accumulator starts at 0)

NB: The empty space acts both as the instruction pointer and as the memory pointer.

<br/>

## The Language
---

### Syntax
Every program consists of two 2D arrays of the same size: first the puzzle, then the commands.  Each line of numbers/commands is comma separated (with no terminating comma).  The puzzle and command arrays must be contiguous blocks separated by at least one newline; otherwise spacing is ignored.  Everything after the command array is ignored. 

### Commands

Every command consists of two opcodes, each of which are a single character.  The first opcodes **must** be a move opcode ('^', 'v', '<', or '>'), but the second command can be anything (including blank, but that's bad style).

| Opcode | Description |
|--------|-------------|
| ^ | Move up one space |
| v | Move down one space |
| < | Move left one space |
| > | Move right one space |
| ? | Read a number **or** single byte character from input to the accumulator|
| ! | Write the value of the accumulator to output |
| X | Write the character with the corresponding ascii value of the accumulator to output |
| 0 | Set the accumulator to 0 |
| _ | No operation|

The following opcodes refer to the memory cell of the piece that just swapped with the empty space.
| Opcode | Description |
|--------|-------------|
| + | Add the value of the memory cell to the accumulator |
| - | Subtract the value of the memory cell from the accumulator |
| * | Multiply the accumulator by the value of the memory cell |
| / | Divide the accumulator by the value of the memory cell (rounding down) |
| @ | Set the accumulator to the value of the memory cell |
| = | Set the value of the memory cell to the accumulator |
| ~ | Swap the accumulator with the value of the memory cell |

### Special Cases
In most instances, a command will be a move opcode followed by a non-move opcode, and would resolve as one would expect.  Double move commands, however, aren't exactly well-defined so far about their behavior.  These are instead special cases that allow for control flow.

| Case | Examples | Description |
|------|---------|-------------|
| Same move opcodes | >>, vv | Move to end of row/col in given direction |
| Different move opcodes | ^v, v< | If the accumulator is non-zero, move in the first direction.  Otherwise move in the second direction |

