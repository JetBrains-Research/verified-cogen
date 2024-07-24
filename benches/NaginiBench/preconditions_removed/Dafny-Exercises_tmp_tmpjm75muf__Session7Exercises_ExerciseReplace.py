from typing import List, Tuple

from nagini_contracts.contracts import *


def replace(v : List[int], x : int, y : int) -> None:
    Ensures(Acc(list_pred(v)))
    Ensures(len(v) == Old(len(v)))
    Ensures(Forall(int, lambda d_0_k_:
        Implies((((0) <= (d_0_k_)) and ((d_0_k_) < (Old(len((v)))))) and ((Old((v)[d_0_k_])) == (x)), ((v)[d_0_k_]) == (y))))
    Ensures(Forall(int, lambda d_1_k_:
        Implies((((0) <= (d_1_k_)) and ((d_1_k_) < (Old(len((v)))))) and ((Old((v)[d_1_k_])) != (x)), ((v)[d_1_k_]) == (Old((v)[d_1_k_])))))
    d_2_i_ = int(0) # type : int
    d_2_i_ = 0
    while (d_2_i_) < (len((v))):
        Invariant(Acc(list_pred(v)))
        Invariant(((0) <= (d_2_i_)) and ((d_2_i_) <= (len((v)))))
        Invariant(len(v) == Old(len(v)))
        Invariant(Forall(int, lambda d_3_k_:
            Implies((((0) <= (d_3_k_)) and ((d_3_k_) < (d_2_i_))) and ((Old((v)[d_3_k_])) == (x)), ((v)[d_3_k_]) == (y))))
        Invariant(Forall(int, lambda d_4_k_:
            Implies(((d_2_i_) <= (d_4_k_)) and ((d_4_k_) < (len((v)))), ((v)[d_4_k_]) == (Old((v)[d_4_k_])))))
        Invariant(Forall(int, lambda d_5_k_:
            Implies((((0) <= (d_5_k_)) and ((d_5_k_) < (d_2_i_))) and ((Old((v)[d_5_k_])) != (x)), ((v)[d_5_k_]) == (Old((v)[d_5_k_])))))
        if ((v)[d_2_i_]) == (x):
            (v)[(d_2_i_)] = y
        d_2_i_ = (d_2_i_) + (1)
