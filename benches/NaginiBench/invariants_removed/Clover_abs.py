from typing import List
from nagini_contracts.contracts import *

def Abs(x : int) -> int:
    Ensures(not ((x) >= (0)) or ((x) == (Result())))
    Ensures(not ((x) < (0)) or (((x) + (Result())) == (0)))
    y = int(0) # type : int
    if (x) < (0):
        y = (0) - (x)
        return y
    elif True:
        y = x
        return y

