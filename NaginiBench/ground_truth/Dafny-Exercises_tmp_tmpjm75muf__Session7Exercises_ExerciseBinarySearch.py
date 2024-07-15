from typing import List, Tuple
from nagini_contracts.contracts import *

@Pure
def sorted(s : List[int]) -> bool :
    Requires(Acc(list_pred(s), 1/2))
    return Forall(int, lambda d_0_u_:
        Forall(int, lambda d_1_w_:
            Implies((((0) <= (d_0_u_)) and ((d_0_u_) < (d_1_w_))) and ((d_1_w_) < (len(s))), ((s)[d_0_u_]) <= ((s)[d_1_w_]))))

def binarySearchRec(v : List[int], elem : int, c : int, f : int) -> int:
    Requires(Acc(list_pred(v), 1/2))
    Requires(sorted(v))
    Requires((((0) <= (c)) and ((c) <= ((f) + (1)))) and (((f) + (1)) <= (len((v)))))
    Requires(Forall(int, lambda d_10_k_:
        Implies(((0) <= (d_10_k_)) and ((d_10_k_) < (c)), ((v)[d_10_k_]) <= (elem))))
    Requires(Forall(int, lambda d_11_k_:
        Implies(((f) < (d_11_k_)) and ((d_11_k_) < (len((v)))), ((v)[d_11_k_]) > (elem))))
    Ensures(Acc(list_pred(v), 1/2))
    Ensures(sorted(v))
    Ensures(len(v) == Old(len(v)))
    Ensures(Forall(int, lambda d_10_k_: Implies(0 <= d_10_k_ and d_10_k_ < len(v), v[d_10_k_] == Old(v)[d_10_k_])))
    Ensures(((-1) <= (Result())) and ((Result()) < (len((v)))) and Result() <= f)
    Ensures((Forall(int, lambda d_12_u_:
        Implies(((0) <= (d_12_u_)) and ((d_12_u_) <= (Result())), ((v)[d_12_u_]) <= (elem)))) and (Forall(int, lambda d_13_w_:
        Implies(((Result()) < (d_13_w_)) and ((d_13_w_) < (len((v)))), ((v)[d_13_w_]) > (elem)))))
    p = int(0) # type : int
    if (c) == ((f) + (1)):
        p = (c) - (1)
    elif True:
        d_14_m_ = int(0) # type : int
        d_14_m_ = ((c) + (f)) // 2
        if ((v)[d_14_m_]) <= (elem):
            out1_ = int(0) # type : int
            out1_ = binarySearchRec(v, elem, (d_14_m_) + (1), f)
            p = out1_
        elif True:
            out2_ = int(0) # type : int
            out2_ = binarySearchRec(v, elem, c, (d_14_m_) - (1))
            p = out2_
    return p

def otherbSearch(v : List[int], elem : int) -> Tuple[bool, int]:
    Requires(Acc(list_pred(v)))
    Requires(sorted(v))
    Ensures(Acc(list_pred(v)))
    Ensures(((0) <= (Result()[1])) and ((Result()[1]) <= (len((v)))))
    Ensures(Implies(Result()[0], ((Result()[1]) < (len((v)))) and (((v)[Result()[1]]) == (elem))))
    Ensures(Implies(not(Result()[0]), (Forall(int, lambda d_15_u_:
        Implies(((0) <= (d_15_u_)) and ((d_15_u_) < (Result()[1])), ((v)[d_15_u_]) < (elem)))) and (Forall(int, lambda d_16_w_:
        Implies(((Result()[1]) <= (d_16_w_)) and ((d_16_w_) < (len((v)))), ((v)[d_16_w_]) > (elem))))))
    Ensures((Result()[0]) == (Exists(int, lambda j: j >= 0 and j < len(v) and v[j] == elem)))
    b = False # type : bool
    p = int(0) # type : int
    out3_ = int(0) # type : int
    out3_ = binarySearchRec(v, elem, 0, len(v) - 1)
    p = out3_
    if (p) == (-1):
        b = False
        p = (p) + (1)
    elif True:
        b = ((v)[p]) == (elem)
        p = (p) + ((0 if b else 1))
    return (b, p)