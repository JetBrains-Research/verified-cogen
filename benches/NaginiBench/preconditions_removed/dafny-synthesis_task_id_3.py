from typing import List, Tuple
from nagini_contracts.contracts import *

def IsNonPrime(n : int) -> bool:
    Ensures(n >= 2)
    Ensures(Implies(Result(), Exists(int, lambda k: 2 <= k and k < n and n % k == 0)))
    Ensures(Implies(not Result(), Forall(int, lambda k: Implies(2 <= k and k < n, n % k != 0))))
    result = bool(False)
    i = int(2)
    while i <= n // 2:
        Invariant(n >= 2)
        Invariant(2 <= i and i <= n // 2 + 1 and i <= n)
        Invariant(Implies(result, Exists(int, lambda k: 2 <= k and k < i and n % k == 0)))
        Invariant(Implies(not result, Forall(int, lambda k: Implies(2 <= k and k < i, n % k != 0))))
        if n % i == 0:
            result = bool(True)
        i = i + 1
    return result