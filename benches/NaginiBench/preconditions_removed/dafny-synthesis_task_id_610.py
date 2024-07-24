from typing import List, Tuple

from nagini_contracts.contracts import *


def RemoveElement(s : List[int], k : int) -> List[int]:
    Ensures(Acc(list_pred(s)))
    Ensures(Acc(list_pred(Result())))
    Ensures((len((Result()))) == ((len((s))) - (1)))
    Ensures(((0) <= (k)) and ((k) < (len((s)))))
    Ensures(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (k)), ((Result())[d_0_i_]) == ((s)[d_0_i_]))))
    Ensures(Forall(int, lambda d_1_i_:
        Implies(((k) <= (d_1_i_)) and ((d_1_i_) < (len((Result())))), ((Result())[d_1_i_]) == ((s)[(d_1_i_) + (1)]))))
    v = [int(0)] * 0 # type : List[int]
    nw0_ = [int(0)] * ((len((s))) - (1)) # type : List[int]
    v = nw0_
    d_2_i_ = int(0) # type : int
    d_2_i_ = 0
    while (d_2_i_) < (k):
        Invariant(Acc(list_pred(v)))
        Invariant(Acc(list_pred(s)))
        Invariant(len(v) == len(s) - 1)
        Invariant(((0) <= (d_2_i_)) and ((d_2_i_) <= (k)))
        Invariant(k < len(s))
        Invariant(k <= len(v))
        Invariant(Forall(int, lambda d_3_j_:
            Implies(((0) <= (d_3_j_)) and ((d_3_j_) < (d_2_i_)), ((v)[d_3_j_]) == ((s)[d_3_j_]))))
        (v)[(d_2_i_)] = (s)[d_2_i_]
        d_2_i_ = (d_2_i_) + (1)
    Assert(Forall(int, lambda d_4_i_:
        Implies(((0) <= (d_4_i_)) and ((d_4_i_) < (k)), ((v)[d_4_i_]) == ((s)[d_4_i_]))))
    while (d_2_i_) < (len((v))):
        Invariant(Acc(list_pred(v)))
        Invariant(Acc(list_pred(s)))
        Invariant(((k) <= (d_2_i_)) and ((d_2_i_) <= (len((v)))))
        Invariant(d_2_i_ < len(s))
        Invariant(len(v) == len(s) - 1)
        Invariant(Forall(int, lambda d_5_j_:
            Implies(((k) <= (d_5_j_)) and ((d_5_j_) < (d_2_i_)), ((v)[d_5_j_]) == ((s)[(d_5_j_) + (1)]))))
        Invariant(Forall(int, lambda d_6_i_:
            Implies(((0) <= (d_6_i_)) and ((d_6_i_) < (k)), ((v)[d_6_i_]) == ((s)[d_6_i_]))))
        (v)[(d_2_i_)] = (s)[(d_2_i_) + (1)]
        d_2_i_ = (d_2_i_) + (1)
    return v