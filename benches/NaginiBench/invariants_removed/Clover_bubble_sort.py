from typing import Callable, List, Type, TypeVar

from nagini_contracts.contracts import *


def BubbleSort(a : List[int]) -> None:
    Requires(Acc(list_pred(a)))
    Ensures(Acc(list_pred(a)))
    Ensures(Forall(int, lambda d_0_i_:
        Forall(int, lambda d_1_j_:
            Implies((((0) <= (d_0_i_)) and ((d_0_i_) < (d_1_j_))) and ((d_1_j_) < (len((a)))), ((a)[d_0_i_]) <= ((a)[d_1_j_])))))
    d_2_i_ = int(0) # type : int
    d_2_i_ = (len((a))) - (1)
    while (d_2_i_) > (0):
        d_7_j_ = int(0) # type : int
        d_7_j_ = 0
        while (d_7_j_) < (d_2_i_):
            if ((a)[d_7_j_]) > ((a)[(d_7_j_) + (1)]):
                index0_ = (d_7_j_) + (1) # type : int
                rhs0_ = (a)[(d_7_j_) + (1)] # type : int
                rhs1_ = (a)[d_7_j_] # type : int
                lhs0_ = a # type : List[int]
                lhs1_ = d_7_j_ # type : int
                lhs2_ = a # type : List[int]
                lhs3_ = (d_7_j_) + (1) # type : int
                lhs0_[lhs1_] = rhs0_
                lhs2_[lhs3_] = rhs1_
            d_7_j_ = (d_7_j_) + (1)
        d_2_i_ = (d_2_i_) - (1)



