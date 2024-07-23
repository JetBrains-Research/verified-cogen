from typing import Dict, List, Optional, Set, Union, cast

from nagini_contracts.contracts import *


def intersperse(numbers: List[int], delimiter: int) -> List[int]:
    Requires(Acc(list_pred(numbers)))
    Ensures(Acc(list_pred(numbers)))
    Ensures(Acc(list_pred(Result())))
    Ensures(Implies(len(numbers) != 0, len(Result()) == len(numbers) * 2 - 1))
    Ensures(Implies(len(numbers) == 0, len(Result()) == 0))
    Ensures(Forall(range(len(Result())), lambda i: i % 2 == 1 or Result()[i] == numbers[i // 2]))
    Ensures(Forall(range(len(Result())), lambda i: i % 2 == 0 or Result()[i] == delimiter))

    res = []  # type: List[int]
    if len(numbers) != 0:
        i = 0
        while i + 1 < len(numbers):
            Invariant(Acc(list_pred(numbers)))
            Invariant(Acc(list_pred(res)))
            Invariant(0 <= i and i < len(numbers))
            Invariant(len(res) == 2 * i)
            Invariant(Forall(range(len(res)), lambda i: i % 2 == 1 or res[i] == numbers[i // 2]))
            Invariant(Forall(range(len(res)), lambda i: i % 2 == 0 or res[i] == delimiter))
            
            res.append(numbers[i])
            res.append(delimiter)
            i += 1
        
        # Append the last element only
        res.append(numbers[i])

    return res