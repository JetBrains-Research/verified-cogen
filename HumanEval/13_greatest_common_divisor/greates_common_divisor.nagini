from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *

def greatest_common_divisor(a: int, b: int) -> int:
    Requires(a != 0 or b != 0)
    Ensures(Result() != 0)

    x = a
    y = b

    while y != 0:
        Invariant(x != 0 or y != 0)
        temp = y
        y = x % y
        x = temp

    return x