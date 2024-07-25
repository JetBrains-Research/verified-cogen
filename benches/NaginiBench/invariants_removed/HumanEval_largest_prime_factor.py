from nagini_contracts.contracts import *

def is_prime(k : int) -> bool:
    Requires(k >= 2)
    Ensures(Implies(Result(), Forall(int, lambda i : Implies((i >= 2) and (i < k), (k % i != 0)))))
    Ensures(Implies(Result() == False, Exists(int, lambda j : ((j >= 2) and (j < k) and (k % j == 0)))))
    i = 2 # type : int
    result = True # type : bool
    while i < k:
        if k % i == 0:
            result = False
        i = i + 1
    return result

@Pure
def is_prime_pred(k : int) -> bool:
    return Forall(int, lambda i : Implies((i >= 2) and (i < k), (k % i != 0)))

def largest_prime_factor(n: int) -> int:
    Requires(n >= 2)
    Ensures(Result() >= 1 and Result() <= n and (Result() == 1 or Result() > 1 and is_prime_pred(Result())))
    largest = 1 # type : int
    j = 2 # type : int
    while j <= n:
        if n % j == 0 and is_prime(j):
            largest = max(largest, j)
        j = j + 1
    return largest