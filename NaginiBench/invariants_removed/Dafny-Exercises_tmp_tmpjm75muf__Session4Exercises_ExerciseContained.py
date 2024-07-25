from typing import List
from nagini_contracts.contracts import *

@Pure
def strictSorted(s : List[int]) -> bool :
    Requires(Acc(list_pred(s)))
    return Forall(int, lambda d_0_u_:
        (Forall(int, lambda d_1_w_:
            (Implies((((0) <= (d_0_u_)) and ((d_0_u_) < (d_1_w_))) and ((d_1_w_) < (len(s))), ((s)[d_0_u_]) < ((s)[d_1_w_])),
               [[(s)[d_1_w_]]])),
            [[(s)[d_0_u_]]]))

def mcontained(v : List[int], w : List[int], n : int, m : int) -> bool:
    Requires(Acc(list_pred(w)))
    Requires(Acc(list_pred(v)))
    Requires(((n) <= (m)) and ((n) >= (0)))
    Requires(strictSorted(v))
    Requires(strictSorted(w))
    Requires(((len((v))) >= (n)) and ((len((w))) >= (m)))
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
        if ((v)[d_3_i_]) == ((w)[d_4_j_]):
            d_3_i_ = (d_3_i_) + (1)
        d_4_j_ = (d_4_j_) + (1)
    b = (d_3_i_) == (n)
    return b

