from typing import List

from nagini_contracts.contracts import *


def append(a : List[int], b : int) -> List[int]:
    Requires(Acc(list_pred(a)))
    Ensures(Acc(list_pred(a)))
    Ensures(Acc(list_pred(Result())))
    Ensures(len(Result()) == len(a) + 1)
    Ensures(Forall(int, lambda i: (Implies(0 <= i and i < len(a), Result()[i] == a[i]))))
    Ensures(Result()[len(a)] == b)
    c = [int(0)] * 0 # type : List[int]
    nw0_ = [int(0)] * (len((a)) + (1)) # type : List[int]
    c = nw0_
    d_0_i_ = int(0) # type : int
    d_0_i_ = 0
    while (d_0_i_) < (len((a))):
        (c)[(d_0_i_)] = (a)[d_0_i_]
        d_0_i_ = (d_0_i_) + (1)
    (c)[(len((a)))] = b
    return c

