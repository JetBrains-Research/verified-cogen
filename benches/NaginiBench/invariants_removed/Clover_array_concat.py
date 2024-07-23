from typing import List

from nagini_contracts.contracts import *


def concat(a : List[int], b : List[int]) -> List[int]:
    Requires(Acc(list_pred(b)))
    Requires(Acc(list_pred(a)))
    Ensures(Acc(list_pred(b)))
    Ensures(Acc(list_pred(a)))
    Ensures(Acc(list_pred(Result())))
    Ensures((len((Result()))) == ((len((b))) + (len((a)))))
    Ensures(Forall(int, lambda d_0_k_:
        Implies(((0) <= (d_0_k_)) and ((d_0_k_) < (len((a)))), ((Result())[d_0_k_]) == ((a)[d_0_k_]))))
    Ensures(Forall(int, lambda d_1_k_:
        Implies(((0) <= (d_1_k_)) and ((d_1_k_) < (len((b)))), ((Result())[(d_1_k_) + (len((a)))]) == ((b)[d_1_k_]))))
    c = [int(0)] * 0 # type : List[int]
    nw0_ = [int(0)] * (len((a)) + len((b))) # type : List[int]
    c = nw0_
    d_2_i_ = int(0) # type : int
    d_2_i_ = 0
    while (d_2_i_) < (len((c))):
        (c)[(d_2_i_)] = ((a)[d_2_i_] if (d_2_i_) < (len((a))) else (b)[(d_2_i_) - (len((a)))])
        d_2_i_ = (d_2_i_) + (1)
    return c


