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
            res.append(numbers[i])
            res.append(delimiter)
            i += 1
        res.append(numbers[i])

    return res