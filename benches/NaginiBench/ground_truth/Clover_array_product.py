from typing import Callable, List, Type, TypeVar

from nagini_contracts.contracts import *


def arrayProduct(a : List[int], b : List[int]) -> List[int]:
    Requires(Acc(list_pred(b)))
    Requires(Acc(list_pred(a)))
    Requires((len((a))) == (len((b))))
    Ensures(Acc(list_pred(b)))
    Ensures(Acc(list_pred(a)))
    Ensures(Acc(list_pred(Result())))
    Ensures((len((Result()))) == (len((a))))
    Ensures((len((a))) == (len((b))))
    Ensures(Forall(int, lambda i:
        Implies(i >= 0 and i < len(a), ((((a)[i]) * ((b)[i])) == ((Result())[i])))))
    c = [int(0)] * 0 # type : List[int]
    nw0_ = [int(0)] * len((a)) # type : List[int]
    c = nw0_
    d_1_i_ = int(0) # type : int
    d_1_i_ = 0
    while (d_1_i_) < (len((a))):
        Invariant(Acc(list_pred(c)))
        Invariant(Acc(list_pred(b)))
        Invariant(Acc(list_pred(a)))
        Invariant((len((c))) == (len((a))))
        Invariant((len((a))) == (len((b))))
        Invariant(((0) <= (d_1_i_)) and ((d_1_i_) <= (len((a)))))
        Invariant(Forall(int, lambda i:
            Implies(i >= 0 and i < d_1_i_, ((((a)[i]) * ((b)[i])) == ((c)[i])))))
        (c)[(d_1_i_)] = ((a)[d_1_i_]) * ((b)[d_1_i_])
        d_1_i_ = (d_1_i_) + (1)
    return c
