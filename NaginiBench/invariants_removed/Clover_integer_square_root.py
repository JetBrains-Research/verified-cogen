from typing import List, TypeVar, Type, Callable
from nagini_contracts.contracts import *

def SquareRoot(N : int) -> int:
    Requires(N >= 0)
    Ensures((((Result()) * (Result())) <= (N)) and ((N) < (((Result()) + (1)) * ((Result()) + (1)))))
    r = int(0) # type : int
    r = 0
    while (((r) + (1)) * ((r) + (1))) <= (N):
        r = (r) + (1)
    return r


