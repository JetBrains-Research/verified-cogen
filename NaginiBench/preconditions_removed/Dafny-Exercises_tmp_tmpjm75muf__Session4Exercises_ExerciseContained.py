from typing import List
from nagini_contracts.contracts import *

@Pure
def strictSorted(s : List[int]) -> bool :
    return Forall(int, lambda d_0_u_:
        (Forall(int, lambda d_1_w_:
            (Implies((((0) <= (d_0_u_)) and ((d_0_u_) < (d_1_w_))) and ((d_1_w_) < (len(s))), ((s)[d_0_u_]) < ((s)[d_1_w_])),
               [[(s)[d_1_w_]]])),
            [[(s)[d_0_u_]]]))

def mcontained(v : List[int], w : List[int], n : int, m : int) -> bool:
    Ensures(Acc(list_pred(w)))
    Ensures(Acc(list_pred(v)))
    Ensures(((n) <= (m)) and ((n) >= (0)))
    Ensures(((len((v))) >= (n)) and ((len((w))) >= (m)))
    Ensures((Result()) == (Forall(int, lambda d_2_k_:
        Implies(((0) <= (d_2_k_)) and ((d_2_k_) < (n)),
                Exists(int, lambda j: j >= 0 and j < m and v[d_2_k_] == w[j])))))
    b = False # type : bool
    d_3_i_ = int(0) # type : int
    d_3_i_ = 0
    d_4_j_ = int(0) # type : int
    d_4_j_ = 0
    while (((d_3_i_) < (n)) and ((d_4_j_) < (m))) and (((v)[d_3_i_]) >= ((w)[d_4_j_])):
        Invariant(Acc(list_pred(w)))
        Invariant(Acc(list_pred(v)))
        Invariant(((n) <= (m)) and ((n) >= (0)))
        Invariant(((len((v))) >= (n)) and ((len((w))) >= (m)))
        Invariant(((0) <= (d_3_i_)) and ((d_3_i_) <= (n)))
        Invariant(((0) <= (d_4_j_)) and ((d_4_j_) <= (m)))
        Invariant(strictSorted(v))
        Invariant(strictSorted(w))
        Invariant(Implies(d_3_i_ < n, Forall(int, lambda j: (Implies(j >= 0 and j < d_4_j_, v[d_3_i_] != w[j]), [[w[j]]]))))
        Invariant(Forall(int, lambda d_5_k_:
            (Implies(((0) <= (d_5_k_)) and ((d_5_k_) < (d_3_i_)),
                    Exists(int, lambda j: (j >= 0 and j < d_4_j_ and v[d_5_k_] == w[j]))), [[v[d_5_k_]]])))
        if ((v)[d_3_i_]) == ((w)[d_4_j_]):
            d_3_i_ = (d_3_i_) + (1)
        d_4_j_ = (d_4_j_) + (1)
    b = (d_3_i_) == (n)
    return b

