from typing import List, TypeVar, Type, Callable
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
        (c)[(d_1_i_)] = ((a)[d_1_i_]) * ((b)[d_1_i_])
        d_1_i_ = (d_1_i_) + (1)
    return c
