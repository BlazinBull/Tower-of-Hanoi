#!/usr/bin/env python3
"""
Towers of Hanoi
Demonstrates recursion (base case + recursive leap of faith) and iteration (ASCII render loop).
"""

import time
import os
import sys

NUM_DISCS  = 4
DELAY      = 0.85
ROD_HEIGHT = NUM_DISCS + 2
ROD_NAMES  = ["A", "B", "C"]

rods: list[list[int]] = [list(range(NUM_DISCS, 0, -1)), [], []]
move_log: list[tuple[int,int,int]] = []
move_count = 0


def hanoi(n: int, src: int, dst: int, depth: int = 0) -> None:
    if n == 1:                                     # BASE CASE
        _move(src, dst, depth)
        return
    other = 3 - src - dst                          # rod not used as src or dst
    hanoi(n - 1, src, other, depth + 1)            # RECURSIVE: move top n-1 aside
    _move(src, dst, depth)                         # move largest disc to destination
    hanoi(n - 1, other, dst, depth + 1)            # RECURSIVE: move n-1 on top


def _move(src: int, dst: int, depth: int) -> None:
    global move_count
    disc = rods[src].pop()
    rods[dst].append(disc)
    move_count += 1
    move_log.append((disc, src, dst))
    render(src, dst, disc, depth)
    if DELAY:
        time.sleep(DELAY)


def disc_str(size: int, width: int) -> str:
    return ("=" * (size * 2 - 1)).center(width)


def render(last_src: int = -1, last_dst: int = -1,
           last_disc: int = -1, depth: int = 0) -> None:
    clear()
    col_w = NUM_DISCS * 2 + 5

    print("  Towers of Hanoi — Python Recursive Demo")
    print("─" * 42)

    for row in range(ROD_HEIGHT, 0, -1):           # ITERATION: top to bottom
        line = ""
        for r in range(3):                         # ITERATION: across each rod
            disc_at_row = rods[r][row - 1] if row <= len(rods[r]) else None
            cell = disc_str(disc_at_row, col_w) if disc_at_row else "|".center(col_w)
            line += cell
        print(line)

    print("═" * (col_w * 3))
    print("".join(f"  {ROD_NAMES[r]}  ".center(col_w) for r in range(3)))

    if last_disc >= 0:
        print(f"\n  Move {move_count:>3}: disc {last_disc}  "
              f"Rod {ROD_NAMES[last_src]} → Rod {ROD_NAMES[last_dst]}  "
              f"(depth {depth})")
    print(f"  Total: {move_count}  |  Optimal: {2**NUM_DISCS - 1}\n")


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_summary() -> None:
    print("Move Log")
    for i, (disc, src, dst) in enumerate(move_log, 1):  # ITERATION: move log
        print(f"  {i:>3}. disc {disc}  {ROD_NAMES[src]} → {ROD_NAMES[dst]}")
    print(f"\n  Solved {NUM_DISCS} discs in {move_count} moves "
          f"(minimum possible: {2**NUM_DISCS - 1})")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
            if 1 <= n <= 8:
                NUM_DISCS = n
                ROD_HEIGHT = n + 2
                rods = [list(range(n, 0, -1)), [], []]
        except ValueError:
            pass

    print("Starting Towers of Hanoi…")
    time.sleep(0.5)
    render()
    if DELAY:
        time.sleep(DELAY)

    hanoi(NUM_DISCS, src=0, dst=2)
    print_summary()