from typing import Dict, List, Optional, Set, Union, cast

from nagini_contracts.contracts import *


def Cubes(a : List[int]) -> None:
    Requires(Acc(list_pred(a)))
    Ensures(Acc(list_pred(a)))
    Ensures(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len((a)))), ((a)[d_0_i_]) == (((d_0_i_) * (d_0_i_)) * (d_0_i_)))))
    d_1_n_ = int(0) # type : int
    d_1_n_ = 0
    d_2_c_ = int(0) # type : int
    d_2_c_ = 0
    d_3_k_ = int(0) # type : int
    d_3_k_ = 1
    d_4_m_ = int(0) # type : int
    d_4_m_ = 6
    while (d_1_n_) < (len((a))):
        Invariant(Acc(list_pred(a)))
        Invariant(((0) <= (d_1_n_)) and ((d_1_n_) <= (len((a)))))
        Invariant(Forall(int, lambda d_5_i_:
            Implies(((0) <= (d_5_i_)) and ((d_5_i_) < (d_1_n_)), ((a)[d_5_i_]) == (((d_5_i_) * (d_5_i_)) * (d_5_i_)))))
        Invariant((d_2_c_) == (((d_1_n_) * (d_1_n_)) * (d_1_n_)))
        Invariant((d_3_k_) == (((((3) * (d_1_n_)) * (d_1_n_)) + ((3) * (d_1_n_))) + (1)))
        Invariant((d_4_m_) == (((6) * (d_1_n_)) + (6)))
        (a)[(d_1_n_)] = d_2_c_
        d_2_c_ = (d_2_c_) + (d_3_k_)
        d_3_k_ = (d_3_k_) + (d_4_m_)
        d_4_m_ = (d_4_m_) + (6)
        d_1_n_ = (d_1_n_) + (1)



