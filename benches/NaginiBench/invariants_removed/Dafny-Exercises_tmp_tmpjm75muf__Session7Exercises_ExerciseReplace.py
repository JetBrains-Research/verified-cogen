from typing import List, Tuple
from nagini_contracts.contracts import *

def replace(v : List[int], x : int, y : int) -> None:
    Requires(Acc(list_pred(v)))
    Ensures(Acc(list_pred(v)))
    Ensures(len(v) == Old(len(v)))
    Ensures(Forall(int, lambda d_0_k_:
        Implies((((0) <= (d_0_k_)) and ((d_0_k_) < (Old(len((v)))))) and ((Old((v)[d_0_k_])) == (x)), ((v)[d_0_k_]) == (y))))
    Ensures(Forall(int, lambda d_1_k_:
        Implies((((0) <= (d_1_k_)) and ((d_1_k_) < (Old(len((v)))))) and ((Old((v)[d_1_k_])) != (x)), ((v)[d_1_k_]) == (Old((v)[d_1_k_])))))
    d_2_i_ = int(0) # type : int
    d_2_i_ = 0
    while (d_2_i_) < (len((v))):
        if ((v)[d_2_i_]) == (x):
            (v)[(d_2_i_)] = y
        d_2_i_ = (d_2_i_) + (1)
