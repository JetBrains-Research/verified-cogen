from typing import Callable, List, Type, TypeVar

from nagini_contracts.contracts import *


def BubbleSort(a : List[int]) -> None:
    Ensures(Acc(list_pred(a)))
    Ensures(Forall(int, lambda d_0_i_:
        Forall(int, lambda d_1_j_:
            Implies((((0) <= (d_0_i_)) and ((d_0_i_) < (d_1_j_))) and ((d_1_j_) < (len((a)))), ((a)[d_0_i_]) <= ((a)[d_1_j_])))))
    d_2_i_ = int(0) # type : int
    d_2_i_ = (len((a))) - (1)
    while (d_2_i_) > (0):
        Invariant(Acc(list_pred(a)))
        Invariant(not ((d_2_i_) < (0)) or ((len((a))) == (0)))
        Invariant(((-1) <= (d_2_i_)) and ((d_2_i_) < (len((a)))))
        Invariant(Forall(int, lambda d_3_ii_:
            Forall(int, lambda d_4_jj_:
                Implies((((d_2_i_) <= (d_3_ii_)) and ((d_3_ii_) < (d_4_jj_))) and ((d_4_jj_) < (len((a)))), ((a)[d_3_ii_]) <= ((a)[d_4_jj_])))))
        Invariant(Forall(int, lambda d_5_k_:
            Forall(int, lambda d_6_k_k_:
                Implies(((((0) <= (d_5_k_)) and ((d_5_k_) <= (d_2_i_))) and ((d_2_i_) < (d_6_k_k_)) and (d_6_k_k_) < (len((a)))), ((a)[d_5_k_]) <= ((a)[d_6_k_k_])))))
        d_7_j_ = int(0) # type : int
        d_7_j_ = 0
        while (d_7_j_) < (d_2_i_):
            Invariant(Acc(list_pred(a)))
            Invariant((((0) < (d_2_i_)) and ((d_2_i_) < (len((a))))) and (((0) <= (d_7_j_)) and ((d_7_j_) <= (d_2_i_))))
            Invariant(Forall(int, lambda d_8_ii_:
                Forall(int, lambda d_9_jj_:
                    Implies((((d_2_i_) <= (d_8_ii_)) and ((d_8_ii_) <= (d_9_jj_))) and ((d_9_jj_) < (len((a)))), ((a)[d_8_ii_]) <= ((a)[d_9_jj_])))))
            Invariant(Forall(int, lambda d_10_k_:
                Forall(int, lambda d_11_k_k_:
                    Implies(((((0) <= (d_10_k_)) and ((d_10_k_) <= (d_2_i_))) and ((d_2_i_) < (d_11_k_k_))) and ((d_11_k_k_) < (len((a)))), ((a)[d_10_k_]) <= ((a)[d_11_k_k_])))))
            Invariant(Forall(int, lambda d_12_k_:
                Implies(((0) <= (d_12_k_)) and ((d_12_k_) <= (d_7_j_)), ((a)[d_12_k_]) <= ((a)[d_7_j_]))))
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



