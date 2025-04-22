from enum import Enum

class ChessColor(Enum):
    WHITE = 1
    BLACK = 2

class ChessDirection(Enum):
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL = 3

class Move:
    src: tuple[int, int]
    dst: tuple[int, int]
    
    def __init__(self, src: tuple[int, int], dst: tuple[int, int]) -> None:
        self.src = src
        self.dst = dst

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Move):
            return NotImplemented
        return self.src == other.src and self.dst == other.dst

    def __repr__(self):
        return f"Move({self.src}, {self.dst})"
    def __str__(self):
        return f"Move({self.src}, {self.dst})"