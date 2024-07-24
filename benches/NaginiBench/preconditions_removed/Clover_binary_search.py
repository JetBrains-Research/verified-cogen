from typing import Dict, List, Optional, Set, Union, cast

from nagini_contracts.contracts import *


def BinarySearch(a : List[int], key : int) -> int:
    Ensures(Acc(list_pred(a)))
    Ensures(((0) <= (Result())) and ((Result()) <= (len((a)))))
    Ensures(Forall(int, lambda d_2_i_:
        not (((0) <= (d_2_i_)) and ((d_2_i_) < (Result()))) or (((a)[d_2_i_]) < (key))))
    Ensures(not ((Result()) == (len((a)))) or (Forall(int, lambda d_3_i_:
        not (((0) <= (d_3_i_)) and ((d_3_i_) < (len((a))))) or (((a)[d_3_i_]) < (key)))))
    Ensures(Forall(int, lambda d_4_i_:
        not (((Result()) <= (d_4_i_)) and ((d_4_i_) < (len((a))))) or (((a)[d_4_i_]) >= (key))))
    n = int(0) # type : int
    d_5_lo_ = int(0) # type : int
    d_6_hi_ = int(0) # type : int
    rhs0_ = 0 # type : int
    rhs1_ = len((a)) # type : int
    d_5_lo_ = rhs0_
    d_6_hi_ = rhs1_
    while (d_5_lo_) < (d_6_hi_):
        Invariant(Acc(list_pred(a)))
        Invariant(Forall(int, lambda d_0_i_:
            Forall(int, lambda d_1_j_:
                not ((((0) <= (d_0_i_)) and ((d_0_i_) < (d_1_j_))) and ((d_1_j_) < (len((a))))) or (((a)[d_0_i_]) <= ((a)[d_1_j_])))))
        Invariant((((0) <= (d_5_lo_)) and ((d_5_lo_) <= (d_6_hi_))) and ((d_6_hi_) <= (len((a)))))
        Invariant(Forall(int, lambda d_7_i_:
            Implies(((0) <= (d_7_i_)) and ((d_7_i_) < (d_5_lo_)), ((a)[d_7_i_]) < (key))))
        Invariant(Forall(int, lambda d_8_i_:
            Implies(((d_6_hi_) <= (d_8_i_)) and ((d_8_i_) < (len((a)))), ((a)[d_8_i_]) >= (key))))
        d_9_mid_ = int(0) # type : int
        d_9_mid_ = ((d_5_lo_) + (d_6_hi_)) // 2
        if ((a)[d_9_mid_]) < (key):
            d_5_lo_ = (d_9_mid_) + (1)
        elif True:
            d_6_hi_ = d_9_mid_
    n = d_5_lo_
    return n

