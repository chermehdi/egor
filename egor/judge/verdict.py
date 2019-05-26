import enum


class Verdict(enum.Enum):
    """
    Enumeration of all possible verdicts produced by the checker
    """
    OK = 1,
    WA = 2,
    PE = 3,
    SK = 4,
    TL = 5
