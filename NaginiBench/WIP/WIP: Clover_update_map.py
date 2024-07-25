from typing import Dict, Set, List
from nagini_contracts.contracts import *

def update__map(m1 : Dict[int, int], m2 : Dict[int, int]) -> Dict[int, int]:
    Requires(Acc(dict_pred(m2)))
    Requires(Acc(dict_pred(m1)))
    Ensures(Acc(dict_pred(m2)))
    Ensures(Acc(dict_pred(m1)))
    Ensures(Acc(dict_pred(Result())))
    # Ensures(Forall(int, lambda d_0_k_:
    #     Implies((d_0_k_) in (m2), (d_0_k_) in (Result()))))
    # Ensures(Forall(int, lambda d_1_k_:
    #     Implies((d_1_k_) in (m1), (d_1_k_) in (Result()))))
    # Ensures(Forall(int, lambda d_2_k_:
    #     Implies((d_2_k_) in (m2), ((Result())[d_2_k_]) == ((m2)[d_2_k_]))))
    # Ensures(Forall(int, lambda d_3_k_:
    #     Implies((not((d_3_k_) in (m2))) and ((d_3_k_) in (m1)), ((Result())[d_3_k_]) == ((m1)[d_3_k_]))))
    # Ensures(Forall(int, lambda d_4_k_:
    #     Implies((not((d_4_k_) in (m2))) and (not((d_4_k_) in (m1))), not((d_4_k_) in (Result())))))
    
    coll0_ : Dict[int, int] = {}
    m1KeysS : Set[int] = set(m1.keys())
    m1Keys : List[int] = list(m1KeysS)
    m2KeysS : List[int] = list(m2.keys())
    m2Keys : List[int] = list(m2KeysS)
    i : int = 0
    while i < len(m1Keys):
        Invariant(Acc(dict_pred(m2)))
        Invariant(Acc(dict_pred(m1)))
        Invariant(Acc(dict_pred(coll0_)))
        Invariant(i >= 0 and i <= len(m1Keys))
        Invariant(Forall(int, lambda j:
            (Implies(j >= 0 and j < i, m1Keys[j] in coll0_), [[m1Keys[j]]])))
        Invariant(Forall(int, lambda j:
            (Implies(j >= 0 and j < i, m1[m1Keys[j]] == coll0_[m1Keys[j]]), [[m1Keys[j]]])))
        d_5_k_ : int = m1Keys[i]
        coll0_[d_5_k_] = (m1)[d_5_k_]
        i = i + 1
    i = 0
    while i < len(m2Keys):
        Invariant(Acc(dict_pred(m2)))
        Invariant(Acc(dict_pred(m1)))
        Invariant(Acc(dict_pred(coll0_)))
        Invariant(i >= 0 and i <= len(m2Keys))
        Invariant(Forall(int, lambda j:
            (Implies(j >= 0 and j < i, m2Keys[j] in coll0_), [[m2Keys[j]]])))
        Invariant(Forall(int, lambda j:
            (Implies(j >= 0 and j < i, m2[m2Keys[j]] == coll0_[m2Keys[j]]), [[m2Keys[j]]])))
        Invariant(Forall(int, lambda j:
            (Implies(j >= 0 and j < len(m1Keys) and not(m1Keys[j] in m2), m1[m1Keys[j]] == coll0_[m1Keys[j]]), [[m1Keys[j]]])))
        d_5_k_ = m2Keys[i]
        coll0_[d_5_k_] = (m2)[d_5_k_]
        i = i + 1
    return coll0_