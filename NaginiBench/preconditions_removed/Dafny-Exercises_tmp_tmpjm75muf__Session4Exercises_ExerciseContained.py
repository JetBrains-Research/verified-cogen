from typing import List
from nagini_contracts.contracts import *

@pure
def strictSorted(s : List[int]) -> bool :
    return Forall(int, lambda d_0_u_:
        Forall(int, lambda d_1_w_:
            Implies((((0) <= (d_0_u_)) and ((d_0_u_) < (d_1_w_))) and ((d_1_w_) < (len(s))), ((s)[d_0_u_]) < ((s)[d_1_w_]))))

def mcontained(v : List[int], w : List[int], n : int, m : int) -> bool:
    Ensures(Acc(list_pred(w)))
    Ensures(Acc(list_pred(v)))
    Ensures((Result()) == (Forall(int, lambda d_2_k_:
        Implies(((0) <= (d_2_k_)) and ((d_2_k_) < (n)), ((v)[d_2_k_]) in (list((w)[:m:]))))))
    b = False # type : bool
    d_3_i_ = int(0) # type : int
    d_3_i_ = 0
    d_4_j_ = int(0) # type : int
    d_4_j_ = 0
    while (((d_3_i_) < (n)) and ((d_4_j_) < (m))) and (((v)[d_3_i_]) >= ((w)[d_4_j_])):
        Invariant(Acc(list_pred(w)))
        Invariant(Acc(list_pred(v)))
        Invariant(((0) <= (d_3_i_)) and ((d_3_i_) <= (n)))
        Invariant(((0) <= (d_4_j_)) and ((d_4_j_) <= (m)))
        Invariant(strictSorted(v))
        Invariant(strictSorted(w))
        Invariant(Forall(int, lambda d_5_k_:
            Implies(((0) <= (d_5_k_)) and ((d_5_k_) < (d_3_i_)), ((v)[d_5_k_]) in (list((w)[:d_4_j_:])))))
        Invariant(not ((d_3_i_) < (n)) or (not(((v)[d_3_i_]) in w)))
        if ((v)[d_3_i_]) == ((w)[d_4_j_]):
            d_3_i_ = (d_3_i_) + (1)
        d_4_j_ = (d_4_j_) + (1)
    Assert(not ((d_3_i_) < (n)) or (not(((v)[d_3_i_]) in w[:m])))
    b = (d_3_i_) == (n)
    return b

