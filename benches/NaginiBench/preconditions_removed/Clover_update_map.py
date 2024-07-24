from typing import Dict, List, Set

from nagini_contracts.contracts import *


def update__map(m1 : Dict[int, int], m2 : Dict[int, int]) -> Dict[int, int]:
    Ensures(Acc(dict_pred(m2)))
    Ensures(Acc(dict_pred(m1)))
    Ensures(Acc(dict_pred(Result())))
    Ensures(Forall(int, lambda d_0_k_:
        Implies((d_0_k_) in (m2), (d_0_k_) in (Result()))))
    Ensures(Forall(int, lambda d_1_k_:
        Implies((d_1_k_) in (m1), (d_1_k_) in (Result()))))
    Ensures(Forall(int, lambda d_2_k_:
        Implies((d_2_k_) in (m2), ((Result())[d_2_k_]) == ((m2)[d_2_k_]))))
    Ensures(Forall(int, lambda d_3_k_:
        Implies((not((d_3_k_) in (m2))) and ((d_3_k_) in (m1)), ((Result())[d_3_k_]) == ((m1)[d_3_k_]))))
    Ensures(Forall(int, lambda d_4_k_:
        Implies((not((d_4_k_) in (m2))) and (not((d_4_k_) in (m1))), not((d_4_k_) in (Result())))))
    
    coll0_ : Dict[int, int] = {}
    m1Keys : Set[int] = set(m1.keys())
    m2Keys : Set[int] = set(m2.keys())
    mUnionS : Set[int] = m1Keys.union(m2Keys)
    mUnion : List[int] = list(mUnionS)
    i : int = 0
    while i < len(mUnion):
        Invariant(Acc(dict_pred(m2)))
        Invariant(Acc(dict_pred(m1)))
        Invariant(Acc(dict_pred(coll0_)))
        Invariant(i >= 0 and i <= len(mUnion))
        Invariant(Forall(int, lambda j: 
            Implies(j < i, mUnion[j] in coll0_)))
        Invariant(Forall(int, lambda j: 
            Implies(j < i and mUnion[j] in m2, m2[mUnion[j]] == coll0_[mUnion[j]])))
        Invariant(Forall(int, lambda j: 
            Implies(j < i and not(mUnion[j] in m2), m1[mUnion[j]] == coll0_[mUnion[j]])))
        d_5_k_ : int = mUnion[i]
        coll0_[d_5_k_] = ((m2)[d_5_k_] if (d_5_k_) in (m2Keys) else (m1)[d_5_k_])
        i += 1
    return coll0_