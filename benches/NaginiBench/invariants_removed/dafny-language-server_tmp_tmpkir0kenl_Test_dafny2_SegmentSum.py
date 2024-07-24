from typing import List, Tuple

from nagini_contracts.contracts import *


@Pure
def Sum(a : List[int], s : int, t : int) -> int :
    Requires(Acc(list_pred(a)))
    Requires((0) <= (s))
    Requires((s) <= (t))
    Requires((t) <= (len(a)))
    if s == t: 
        return 0
    else:
        return a[t - 1] + Sum(a, s, t - 1)

def MaxSegSum(a : List[int]) -> Tuple[int, int]:
    Requires(Acc(list_pred(a)))
    Ensures(Acc(list_pred(a)))
    Ensures((((0) <= (Result()[0])) and ((Result()[0]) <= (Result()[1]))) and ((Result()[1]) <= (len(a))))
    Ensures(Forall(int, lambda d_1_p_:
        Forall(int, lambda d_2_q_:
            Implies((((0) <= (d_1_p_)) and ((d_1_p_) <= (d_2_q_))) and ((d_2_q_) <= (len(a))), (Sum(a, d_1_p_, d_2_q_)) <= (Sum(a, Result()[0], Result()[1]))))))
    k = int(0) # type : int
    m = int(0) # type : int
    rhs0_ = 0 # type : int
    rhs1_ = 0 # type : int
    k = rhs0_
    m = rhs1_
    d_3_s_ = int(0) # type : int
    d_3_s_ = 0
    d_4_n_ = int(0) # type : int
    d_4_n_ = 0
    d_5_c_ = int(0) # type : int
    d_6_t_ = int(0) # type : int
    rhs2_ = 0 # type : int
    rhs3_ = 0 # type : int
    d_5_c_ = rhs2_
    d_6_t_ = rhs3_
    while (d_4_n_) < (len(a)):
        rhs4_ = (d_6_t_) + ((a)[d_4_n_]) # type : int
        rhs5_ = (d_4_n_) + (1) # type : int
        d_6_t_ = rhs4_
        d_4_n_ = rhs5_
        if (d_6_t_) < (0):
            rhs6_ = d_4_n_ # type : int
            rhs7_ = 0 # type : int
            d_5_c_ = rhs6_
            d_6_t_ = rhs7_
        elif (d_3_s_) < (d_6_t_):
            rhs8_ = d_5_c_ # type : int
            rhs9_ = d_4_n_ # type : int
            rhs10_ = d_6_t_ # type : int
            k = rhs8_
            m = rhs9_
            d_3_s_ = rhs10_
    return (k, m)