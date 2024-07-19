from typing import List, Tuple
from nagini_contracts.contracts import *

@Pure
def getSize(i : int, j : int) -> int :
    return ((j) - (i)) + (1)

def longestZero(a : List[int]) -> Tuple[int, int]:
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
        Invariant(Acc(list_pred(d_4_b_)))
        Invariant(Acc(list_pred(a)))
        Invariant((1) <= (len((a))))
        Invariant(len(a) == len(d_4_b_))
        Invariant(((0) <= (d_5_idx_)) and ((d_5_idx_) <= ((len((a))) - (1))))
        Invariant(Forall(int, lambda d_6_i_:
            Implies(((0) <= (d_6_i_)) and ((d_6_i_) <= (d_5_idx_)), ((0) <= ((d_4_b_)[d_6_i_])))))
        Invariant(Forall(int, lambda d_6_i_:
            Implies(((0) <= (d_6_i_)) and ((d_6_i_) <= (d_5_idx_)), (((d_4_b_)[d_6_i_]) <= (d_5_idx_ + 1)))))
        Invariant(Forall(int, lambda d_6_i_:
            Implies(((0) <= (d_6_i_)) and ((d_6_i_) <= (d_5_idx_)), (((d_4_b_)[d_6_i_]) <= (d_6_i_ + 1)) )))
        Invariant(Forall(int, lambda i : Implies(i >= 0 and i <= d_5_idx_, Forall(int, lambda j : Implies(j >= i - 1 and j <= d_5_idx_ + 1, j - i >= -1)))))
        Invariant(Forall(int, lambda d_7_i_:
            Implies(((0) <= (d_7_i_)) and ((d_7_i_) <= (d_5_idx_)), (-1) <= ((d_7_i_) - ((d_4_b_)[d_7_i_])))))
        Invariant(Forall(int, lambda d_8_i_:
            Implies(((0) <= (d_8_i_)) and ((d_8_i_) <= (d_5_idx_)), Forall(int, lambda d_9_j_:
                Implies((((d_8_i_) - ((d_4_b_)[d_8_i_])) < (d_9_j_)) and ((d_9_j_) <= (d_8_i_)), ((a)[d_9_j_]) == (0))))))
        Invariant(Forall(int, lambda d_10_i_:
            Implies(((0) <= (d_10_i_)) and ((d_10_i_) <= (d_5_idx_)), Implies((0) <= ((d_10_i_) - ((d_4_b_)[d_10_i_])), (d_10_i_) - ((d_4_b_)[d_10_i_]) >= 0 and (d_10_i_) - ((d_4_b_)[d_10_i_]) < len(a) and ((a)[(d_10_i_) - ((d_4_b_)[d_10_i_])]) != (0)))))
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
        Invariant(Acc(list_pred(d_4_b_)))
        Invariant(Acc(list_pred(a)))
        Invariant((1) <= (len((a))))
        Invariant(len(a) == len(d_4_b_))
        Invariant(((1) <= (d_5_idx_)) and ((d_5_idx_) <= (len((d_4_b_)))))
        Invariant(Forall(int, lambda d_6_i_:
            Implies(((0) <= (d_6_i_)) and ((d_6_i_) < (len(a))), (((d_4_b_)[d_6_i_]) <= (d_6_i_ + 1)))))
        Invariant(((0) <= (sz)) and ((sz) <= (len((a)))))
        Invariant(((0) <= (pos)) and ((pos) < (len((a)))))
        Invariant(((pos) + (sz)) <= (len((a))))
        Invariant(((pos) + (sz)) - 1 <= (len((a))) - 1)
        Invariant(Forall(int, lambda d_11_i_:
            Implies(((0) <= (d_11_i_)) and ((d_11_i_) < (d_5_idx_)), ((d_4_b_)[d_11_i_]) <= (sz))))
        Invariant(Forall(int, lambda d_8_i_:
            Implies(((0) <= (d_8_i_)) and ((d_8_i_) <= (len(a) - 1)), Forall(int, lambda d_9_j_:
                Implies((((d_8_i_) - ((d_4_b_)[d_8_i_])) < (d_9_j_)) and ((d_9_j_) <= (d_8_i_)), ((a)[d_9_j_]) == (0))))))
        
        Invariant(Forall(int, lambda d_12_i_:
            Implies(((pos - 1) < (d_12_i_)) and ((d_12_i_) <= ((pos) + (sz)) - 1), ((a)[d_12_i_]) == (0))))
        if ((d_4_b_)[d_5_idx_]) > (sz):
            sz = (d_4_b_)[d_5_idx_]
            pos = ((d_5_idx_) - ((d_4_b_)[d_5_idx_])) + (1)
        d_5_idx_ = (d_5_idx_) + (1)
    return (sz, pos)

