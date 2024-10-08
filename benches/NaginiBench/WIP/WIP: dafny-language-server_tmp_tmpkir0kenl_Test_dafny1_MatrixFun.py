from typing import List
from nagini_contracts.contracts import *

@Pure
def inner_Forall(d_14_i_ : int, a : List[List[int]], b : List[List[int]]) -> bool:
    Requires(Acc(list_pred(a)))
    Requires(Forall(a, lambda m0: Acc(list_pred(m0))))
    Requires(Acc(list_pred(b)))
    Requires(Forall(b, lambda m0: Acc(list_pred(m0))))
    Requires(len(a) > 0)
    Requires(len(a) == len(b))
    Requires((len((a))) == (len((a)[0])))
    Requires((len((b))) == (len((b)[0])))
    Requires(Forall(int, lambda d_0_i_: Implies(d_0_i_ >= 0 and d_0_i_ < len(a), len(a[0]) == len(a[d_0_i_]))))
    return Forall(int, lambda d_15_j_:
        (Implies((((0) <= (d_14_i_)) and ((d_14_i_) < (len((a))))) and (((0) <= (d_15_j_)) and ((d_15_j_) < (len((a)[0])))),
                (a[d_14_i_][d_15_j_]) == (b[d_15_j_][d_14_i_])), [[a[d_14_i_][d_15_j_]]]))



def Flip(m : List[List[int]]) -> None:
    Requires(Acc(list_pred(m)))
    Requires(Forall(m, lambda m0: Acc(list_pred(m0))))
    Requires(len(m) > 0)
    Requires((len((m))) == (len((m)[0])))
    Requires(Forall(int, lambda d_0_i_: Implies(d_0_i_ >= 0 and d_0_i_ < len(m), len(m[0]) == len(m[d_0_i_]))))
    Ensures(Acc(list_pred(m)))
    Ensures(Forall(m, lambda m0: Acc(list_pred(m0))))
    Ensures(len(m) > 0)
    Ensures(len(m) == Old(len(m)))
    Ensures(Forall(int, lambda i: Implies(i >= 0 and i < len(m), len(m[i]) == Old(len(m[i])))))
    Ensures((len((m))) == (len((m)[0])))
    Ensures(Forall(int, lambda d_0_i_: Implies(d_0_i_ >= 0 and d_0_i_ < len(m), len(m[0]) == len(m[d_0_i_]))))
    # Ensures(Forall(int, lambda d_14_i_:
    #     Forall(int, lambda d_15_j_:
    #         Implies((((0) <= (d_14_i_)) and ((d_14_i_) < (len((m))))) and (((0) <= (d_15_j_)) and ((d_15_j_) < (len((m)[0])))),
    #                 ((m)[d_14_i_][d_15_j_]) == (Old((m)[d_15_j_][d_14_i_]))))))
    d_16_N_ = int(0) # type : int
    d_16_N_ = len((m))
    d_17_a_ = int(0) # type : int
    d_17_a_ = 0
    d_18_b_ = int(0) # type : int
    d_18_b_ = 1
    m_old = list(m)
    while (d_17_a_) != (d_16_N_):
        Invariant(Acc(list_pred(m)))
        Invariant(Forall(m, lambda m0: Acc(list_pred(m0))))
        Invariant(Acc(list_pred(m_old)))
        Invariant(Forall(m_old, lambda m0: Acc(list_pred(m0))))
        Invariant(len(m) > 0)
        Invariant((len((m))) == (len((m)[0])))
        Invariant(Forall(int, lambda d_0_i_: (Implies(d_0_i_ >= 0 and d_0_i_ < len(m), len(m[0]) == len(m[d_0_i_])), [[m[d_0_i_]]])))
        Invariant(len(m) == (len(m_old)))
        Invariant(Forall(int, lambda i: (Implies(i >= 0 and i < len(m), len(m[i]) == (len(m_old[i]))), [[m[i]]])))
        Invariant(d_17_a_ >= 0)
        Invariant((((d_17_a_) < (d_18_b_)) and ((d_18_b_) <= (d_16_N_)) or 
                   ((d_17_a_) == (d_16_N_)) and ((d_18_b_) == ((d_16_N_) + (1)))))
        Invariant(Forall(int, lambda d_19_i_:
            (inner_Forall(d_19_i_, m, m_old)
                # Forall(int, lambda d_20_j_:
                # (Implies((((0) <= (d_19_i_)) and ((d_19_i_) <= (d_20_j_))) and ((d_20_j_) < (d_16_N_)),
                #         ((((m)[d_19_i_][d_20_j_]) == (Old((m)[d_20_j_][d_19_i_])) and ((m)[d_20_j_][d_19_i_]) == (Old((m)[d_19_i_][d_20_j_]))) if (((d_19_i_) < (d_17_a_)) or (((d_19_i_) == (d_17_a_)) and ((d_20_j_) < (d_18_b_)))) else (((m)[d_19_i_][d_20_j_]) == (Old((m)[d_19_i_][d_20_j_])) and ((m)[d_20_j_][d_19_i_]) == (Old((m)[d_20_j_][d_19_i_])))))
                #  ,[[(m)[d_19_i_][d_20_j_]]]
                #  ))
               ,[[inner_Forall(d_19_i_, m, m_old)]]
             )))
        if (d_18_b_) < (d_16_N_):
            rhs0_ = m[d_18_b_][d_17_a_] # type : int
            m[d_18_b_][d_17_a_] = m[d_17_a_][d_18_b_]
            m[d_17_a_][d_18_b_] = rhs0_
            # Assert(Forall(int, lambda d_19_i_:
            #     (Forall(int, lambda d_20_j_:
            #         (Implies((((0) <= (d_19_i_)) and ((d_19_i_) <= (d_20_j_))) and ((d_20_j_) < (d_16_N_)),
            #             ((((m)[d_19_i_][d_20_j_]) == (Old((m)[d_20_j_][d_19_i_])) and ((m)[d_20_j_][d_19_i_]) == (Old((m)[d_19_i_][d_20_j_]))) if (((d_19_i_) < (d_17_a_)) or (((d_19_i_) == (d_17_a_)) and ((d_20_j_) <= (d_18_b_)))) else (((m)[d_19_i_][d_20_j_]) == (Old((m)[d_19_i_][d_20_j_])) and ((m)[d_20_j_][d_19_i_]) == (Old((m)[d_20_j_][d_19_i_])))))
            #         #,[[(m)[d_19_i_][d_20_j_]]]
            #          ))
            #      #,[[(m)[d_19_i_]]]
            #      )))
            d_18_b_ = (d_18_b_) + (1)
        elif True:
            d_17_a_ = (d_17_a_) + (1)
            d_18_b_ = (d_17_a_) + (1)
            # Assert(Forall(int, lambda d_19_i_:
            #     (Forall(int, lambda d_20_j_:
            #         (Implies((((0) <= (d_19_i_)) and ((d_19_i_) <= (d_20_j_))) and ((d_20_j_) < (d_16_N_)),
            #             ((((m)[d_19_i_][d_20_j_]) == (Old((m)[d_20_j_][d_19_i_])) and ((m)[d_20_j_][d_19_i_]) == (Old((m)[d_19_i_][d_20_j_]))) if (((d_19_i_) < (d_17_a_)) or (((d_19_i_) == (d_17_a_)) and ((d_20_j_) <= (d_18_b_)))) else (((m)[d_19_i_][d_20_j_]) == (Old((m)[d_19_i_][d_20_j_])) and ((m)[d_20_j_][d_19_i_]) == (Old((m)[d_20_j_][d_19_i_])))))
            #         #,[[(m)[d_19_i_][d_20_j_]]]
            #          ))
            #      #,[[(m)[d_19_i_]]]
            #      )))
