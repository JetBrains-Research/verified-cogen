from typing import List, TypeVar, Type, Callable
from nagini_contracts.contracts import *

def iter__copy(s : List[int]) -> List[int]:
    Requires(Acc(list_pred(s)))
    Ensures(Acc(list_pred(s)))
    Ensures(Acc(list_pred(Result())))
    Ensures((len((s))) == (len((Result()))))
    Ensures(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len((s)))), ((s)[d_0_i_]) == ((Result())[d_0_i_]))))
    t = [int(0)] * 0 # type : List[int]
    nw0_ = [int(0)] * len((s)) # type : List[int]
    t = nw0_
    d_1_i_ = int(0) # type : int
    d_1_i_ = 0
    while (d_1_i_) < (len((s))):
        Invariant(Acc(list_pred(t)))
        Invariant(Acc(list_pred(s)))
        Invariant(((0) <= (d_1_i_)) and ((d_1_i_) <= (len((s)))))
        Invariant((len((s))) == (len((t))))
        Invariant(Forall(int, lambda d_2_x_:
            Implies(((0) <= (d_2_x_)) and ((d_2_x_) < (d_1_i_)), ((s)[d_2_x_]) == ((t)[d_2_x_]))))
        (t)[(d_1_i_)] = (s)[d_1_i_]
        d_1_i_ = (d_1_i_) + (1)
    return t

