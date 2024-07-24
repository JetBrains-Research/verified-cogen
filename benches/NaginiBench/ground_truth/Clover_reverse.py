from typing import List

from nagini_contracts.contracts import *


def reverse(a : List[int]) -> None:
    Requires(Acc(list_pred(a)))
    Ensures(Acc(list_pred(a)))
    Ensures(len(a) == Old(len(a)))
    Ensures(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len((a)))), ((a)[d_0_i_]) == (Old((a)[len(a) - 1 - d_0_i_])))))
    d_1_i_ = int(0) # type : int
    d_1_i_ = 0
    while (d_1_i_) < ((len((a)) // 2)):
        Invariant(Acc(list_pred(a)))
        Invariant(len(a) == Old(len(a)))
        Invariant(((0) <= (d_1_i_)) and ((d_1_i_) <= ((len((a)) // 2))))
        Invariant(Forall(int, lambda d_2_k_:
            Implies((((0) <= (d_2_k_)) and ((d_2_k_) < (d_1_i_))) or (((((len((a))) - (1)) - (d_1_i_)) < (d_2_k_)) and ((d_2_k_) <= ((len((a))) - (1)))), ((a)[d_2_k_]) == (Old((a)[((len((a))) - (1)) - (d_2_k_)])))))
        Invariant(Forall(int, lambda d_3_k_:
            Implies(((d_1_i_) <= (d_3_k_)) and ((d_3_k_) <= (((len((a))) - (1)) - (d_1_i_))), ((a)[d_3_k_]) == (Old((a)[d_3_k_])))))
        index0_ = ((len((a))) - (1)) - (d_1_i_) # type : int
        vr = a[index0_] # type : int
        a[index0_] = a[d_1_i_]
        a[d_1_i_] = vr
        d_1_i_ = (d_1_i_) + (1)
