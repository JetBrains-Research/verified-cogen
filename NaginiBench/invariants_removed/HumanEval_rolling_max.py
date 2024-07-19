from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *

@Pure
def getVal(mx: Optional[int]) -> int:
    Requires(mx is not None)  
    return mx  

def rolling_max(numbers: List[int]) -> List[int]:
    Requires(Acc(list_pred(numbers)))
    Ensures(Acc(list_pred(numbers)))
    Ensures(Acc(list_pred(Result())))
    Ensures(len(Result()) == len(numbers))
    Ensures(Forall(range(len(numbers)), lambda i: numbers[i] <= Result()[i]))
    Ensures(Forall(range(len(numbers) - 1), lambda i: Result()[i] <= Result()[i + 1]))

    running_max = None # type: Optional[int]
    result = [] # type: List[int]

    i = 0
    while i < len(numbers):
        n = numbers[i]
        if running_max is None or running_max < n:
            running_max = n
        
        result.append(running_max)
        i += 1

    return result