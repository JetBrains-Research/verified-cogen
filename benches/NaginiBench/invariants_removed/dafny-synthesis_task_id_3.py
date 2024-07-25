from typing import List, Tuple
from nagini_contracts.contracts import *

def IsNonPrime(n : int) -> bool:
    Requires(n >= 2)
    Ensures(n >= 2)
    Ensures(Implies(Result(), Exists(int, lambda k: 2 <= k and k < n and n % k == 0)))
    Ensures(Implies(not Result(), Forall(int, lambda k: Implies(2 <= k and k < n, n % k != 0))))
    result = bool(False)
    i = int(2)
    while i <= n // 2:
        if n % i == 0:
            result = bool(True)
        i = i + 1
    return result