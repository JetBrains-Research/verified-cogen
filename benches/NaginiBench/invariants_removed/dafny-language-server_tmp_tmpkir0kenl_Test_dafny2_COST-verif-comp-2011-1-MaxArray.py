from typing import List

from nagini_contracts.contracts import *


def max(a : List[int]) -> int:
    Requires(Acc(list_pred(a)))
    Requires((len((a))) != (0))
    Ensures(Acc(list_pred(a)))
    Ensures(((0) <= (Result())) and ((Result()) < (len((a)))))
    Ensures(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len((a)))), ((a)[d_0_i_]) <= ((a)[Result()]))))
    x = int(0) # type : int
    x = 0
    d_1_y_ = int(0) # type : int
    d_1_y_ = (len((a))) - (1)
    d_2_m_ = d_1_y_ # type : int
    while (x) != (d_1_y_):
        if ((a)[x]) <= ((a)[d_1_y_]):
            x = (x) + (1)
            d_2_m_ = d_1_y_
        elif True:
            d_1_y_ = (d_1_y_) - (1)
            d_2_m_ = x
    x = x
    return x