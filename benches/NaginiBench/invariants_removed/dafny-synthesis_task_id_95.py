from typing import List, Tuple

from nagini_contracts.contracts import *


def SmallestListLength(s : List[List[int]]) -> int:
    Requires(Acc(list_pred(s)))
    Requires(Forall(s, lambda s1:  Acc(list_pred(s1))))
    Requires((len(s)) > (0))
    Ensures(Acc(list_pred(s)))
    Ensures(Forall(s, lambda s1:  Acc(list_pred(s1))))
    Ensures(s == Old(s))
    Ensures(len(s) > 0)
    Ensures(Forall(s, lambda s1:  s1 == Old(s1)))
    Ensures(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(s))), (Result()) <= (len((s)[d_0_i_])))))
    Ensures(Exists(int, lambda d_1_i_:
        (((0) <= (d_1_i_)) and ((d_1_i_) < (len(s)))) and ((Result()) == (len((s)[d_1_i_])))))
    v = int(0) # type : int
    v = len((s)[0])
    d_2_i_ = int(1) # type : int
    while d_2_i_ < len(s):
        if (len((s)[d_2_i_])) < (v):
            v = len((s)[d_2_i_])
        d_2_i_ = d_2_i_ + 1
    return v