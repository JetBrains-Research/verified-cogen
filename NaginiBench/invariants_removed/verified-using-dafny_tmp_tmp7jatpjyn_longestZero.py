from typing import List, Tuple
from nagini_contracts.contracts import *

@Pure
def getSize(i : int, j : int) -> int :
    return ((j) - (i)) + (1)

def longestZero(a : List[int]) -> Tuple[int, int]:
    Requires(Acc(list_pred(a)))
    Requires((1) <= (len((a))))
    Ensures(Acc(list_pred(a)))
    Ensures(((0) <= (Result()[0])) and ((Result()[0]) <= (len((a)))))
    Ensures(((0) <= (Result()[1])) and ((Result()[1]) < (len((a)))))
    Ensures(((Result()[1]) + (Result()[0])) <= (len((a))))
    Ensures(Forall(int, lambda d_0_i_:
        Implies(((Result()[1] - 1) < (d_0_i_)) and ((d_0_i_) <= ((Result()[1]) + (Result()[0])) - 1), ((a)[d_0_i_]) == (0))))
    sz = int(0) # type : int
    pos = int(0) # type : int
    d_4_b_ = [int(0)] * len((a)) # type : List[int]
    if ((a)[0]) == (0):
        (d_4_b_)[(0)] = 1
    else:
        (d_4_b_)[(0)] = 0
    d_5_idx_ = int(0) # type : int
    d_5_idx_ = 0
    while (d_5_idx_) < ((len((a))) - (1)):
        index1_ = (d_5_idx_) + (1) # type : int
        if ((a)[index1_]) == (0):
            (d_4_b_)[index1_] = ((d_4_b_)[d_5_idx_]) + (1)
        elif True:
            (d_4_b_)[index1_] = 0
        Assert((d_4_b_)[index1_] <= d_5_idx_ + 2)
        Assert((d_4_b_)[index1_] <= index1_ + 1)
        d_5_idx_ = (d_5_idx_) + (1)
    d_5_idx_ = 1
    sz = (d_4_b_)[0]
    pos = 0
    while (d_5_idx_) < (len((a))):
        if ((d_4_b_)[d_5_idx_]) > (sz):
            sz = (d_4_b_)[d_5_idx_]
            pos = ((d_5_idx_) - ((d_4_b_)[d_5_idx_])) + (1)
        d_5_idx_ = (d_5_idx_) + (1)
    return (sz, pos)

