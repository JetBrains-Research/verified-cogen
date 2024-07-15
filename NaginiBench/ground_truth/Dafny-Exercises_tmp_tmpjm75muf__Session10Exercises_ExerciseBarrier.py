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
        Invariant(Acc(list_pred(v)))
        Invariant(((0) <= (p)) and ((p) < (len((v)))))
        Invariant(((0) <= (d_2_i_)) and ((d_2_i_) <= ((p) + (1))))
        Invariant(((0) <= (d_3_max_)) and ((d_3_max_) < (d_2_i_)))
        Invariant(Forall(int, lambda d_4_k_:
            Implies(((0) <= (d_4_k_)) and ((d_4_k_) < (d_2_i_)), ((v)[d_3_max_]) >= ((v)[d_4_k_]))))
        #decreases p - i
        if ((v)[d_2_i_]) > ((v)[d_3_max_]):
            d_3_max_ = d_2_i_
        d_2_i_ = (d_2_i_) + (1)
    while ((d_2_i_) < (len((v)))) and (((v)[d_2_i_]) > ((v)[d_3_max_])):
        Invariant(Acc(list_pred(v)))
        Invariant(((0) <= (p)) and ((p) < (len((v)))))
        Invariant(((0) <= (d_3_max_)) and ((d_3_max_) <= (p)))
        Invariant((p < (d_2_i_)) and ((d_2_i_) <= (len((v)))))
        Invariant(Forall(int, lambda d_5_k_:
            Implies(((0) <= (d_5_k_)) and ((d_5_k_) <= (p)), ((v)[d_5_k_]) <= ((v)[d_3_max_]))))
        Invariant(Forall(int, lambda d_6_k_:
            Implies(((p) < (d_6_k_)) and ((d_6_k_) < (d_2_i_)), ((v)[d_6_k_]) > ((v)[d_3_max_]))))
        #decreases v.Length - i
        d_2_i_ = (d_2_i_) + (1)
    b = (d_2_i_) == (len((v)))
    return b