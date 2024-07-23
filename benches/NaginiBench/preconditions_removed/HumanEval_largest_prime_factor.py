from nagini_contracts.contracts import *


def is_prime(k : int) -> bool:
    Ensures(Implies(Result(), Forall(int, lambda i : Implies((i >= 2) and (i < k), (k % i != 0)))))
    Ensures(Implies(Result() == False, Exists(int, lambda j : ((j >= 2) and (j < k) and (k % j == 0)))))
    i = 2 # type : int
    result = True # type : bool
    while i < k:
        Invariant(i >= 2 and i <= k)
        Invariant(Implies(result == False, Exists(int, lambda j : ((j >= 2) and (j < i) and (k % j == 0)))))
        Invariant(Implies(result, Forall(int, lambda j : Implies((j >= 2) and (j < i), (k % j != 0)))))
        if k % i == 0:
            result = False
        i = i + 1
    return result

@Pure
def is_prime_pred(k : int) -> bool:
    return Forall(int, lambda i : Implies((i >= 2) and (i < k), (k % i != 0)))

def largest_prime_factor(n: int) -> int:
    Ensures(Result() >= 1 and Result() <= n and (Result() == 1 or Result() > 1 and is_prime_pred(Result())))
    largest = 1 # type : int
    j = 2 # type : int
    while j <= n:
        Invariant(j >= 2 and j <= n + 1)
        Invariant(largest >= 1 and largest < j)
        Invariant(largest == 1 or largest > 1 and is_prime_pred(largest))
        if n % j == 0 and is_prime(j):
            largest = max(largest, j)
        j = j + 1
    return largest