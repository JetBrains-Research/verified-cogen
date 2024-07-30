from typing import List
from nagini_contracts.contracts import *

def barrier(v : List[int], p : int) -> bool:
    Requires(Acc(list_pred(v)))
    Requires((len((v))) > (0))
    Requires(((0) <= (p)) and ((p) < (len((v)))))
    Ensures(Acc(list_pred(v)))
    Ensures((Result()) == (Forall(int, lambda d_0_k_:
        Forall(int, lambda d_1_l_:
            Implies((((0) <= (d_0_k_)) and ((d_0_k_) <= (p))) and (((p) < (d_1_l_)) and ((d_1_l_) < (len((v))))), 
                    ((v)[d_0_k_]) < ((v)[d_1_l_]))))))
    b = False # type : bool
    d_2_i_ = int(0) # type : int
    d_2_i_ = 1
    d_3_max_ = int(0) # type : int
    d_3_max_ = 0
    while (d_2_i_) <= (p):
        if ((v)[d_2_i_]) > ((v)[d_3_max_]):
            d_3_max_ = d_2_i_
        d_2_i_ = (d_2_i_) + (1)
    while ((d_2_i_) < (len((v)))) and (((v)[d_2_i_]) > ((v)[d_3_max_])):
        d_2_i_ = (d_2_i_) + (1)
    b = (d_2_i_) == (len((v)))
    return b