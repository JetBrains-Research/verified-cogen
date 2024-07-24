from typing import List, Tuple

from nagini_contracts.contracts import *


def swap(a : List[bool], i : int, j : int) -> None:
    Ensures(Acc(list_pred(a)))
    Ensures((((0) <= (i)) and ((i) < (j))) and ((j) < (len((a)))))
    Ensures(((a)[i]) == (Old((a)[j])))
    Ensures(((a)[j]) == (Old((a)[i])))
    Ensures(len(a) == Old(len(a)))
    Ensures(Forall(int, lambda d_0_m_:
        Implies(((((0) <= (d_0_m_)) and ((d_0_m_) < (len((a))))) and ((d_0_m_) != (i))) and ((d_0_m_) != (j)), ((a)[d_0_m_]) == (Old((a)[d_0_m_])))))
    d_1_t_ = int(0) # type : int
    d_1_t_ = (a)[i]
    (a)[(i)] = (a)[j]
    (a)[(j)] = d_1_t_

def two__way__sort(a : List[bool]) -> None:
    Ensures(Acc(list_pred(a)))
    Ensures(Forall(int, lambda d_2_m_:
        Forall(int, lambda d_3_n_:
            Implies((((0) <= (d_2_m_)) and ((d_2_m_) < (d_3_n_))) and ((d_3_n_) < (len((a)))), (not((a)[d_2_m_])) or ((a)[d_3_n_])))))
    d_4_i_ = int(0) # type : int
    d_4_i_ = 0
    d_5_j_ = int(0) # type : int
    d_5_j_ = (len((a))) - (1)
    while (d_4_i_) <= (d_5_j_):
        Invariant(Acc(list_pred(a)))
        Invariant((((0) <= (d_4_i_)) and ((d_4_i_) <= ((d_5_j_) + (1)))) and (((d_5_j_) + (1)) <= (len((a)))))
        Invariant(Forall(int, lambda d_6_m_:
            Implies(((0) <= (d_6_m_)) and ((d_6_m_) < (d_4_i_)), not((a)[d_6_m_]))))
        Invariant(Forall(int, lambda d_7_n_:
            Implies(((d_5_j_) < (d_7_n_)) and ((d_7_n_) < (len((a)))), (a)[d_7_n_])))
        if not((a)[d_4_i_]):
            d_4_i_ = (d_4_i_) + (1)
        elif (a)[d_5_j_]:
            d_5_j_ = (d_5_j_) - (1)
        elif True:
            swap(a, d_4_i_, d_5_j_)
            d_4_i_ = (d_4_i_) + (1)
            d_5_j_ = (d_5_j_) - (1)