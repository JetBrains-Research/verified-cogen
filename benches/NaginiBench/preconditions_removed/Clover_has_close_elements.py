from typing import Dict, List, Optional, Set, Union, cast

from nagini_contracts.contracts import *


def has__close__elements(numbers : List[int], threshold : int) -> bool:
    Ensures(Acc(list_pred(numbers)))
    Ensures(not (not(Result())) or (Forall(int, lambda d_2_i_:
        Forall(int, lambda d_3_j_:
            Implies((((1) <= (d_2_i_)) and ((d_2_i_) < (len(numbers)))) and (((0) <= (d_3_j_)) and ((d_3_j_) < (d_2_i_))), ((((numbers)[d_3_j_]) - ((numbers)[d_2_i_]) if (((numbers)[d_2_i_]) - ((numbers)[d_3_j_])) < (0) else ((numbers)[d_2_i_]) - ((numbers)[d_3_j_]))) >= (threshold))))))
    res = False # type : bool
    res = False
    d_4_idx_ = int(0) # type : int
    d_4_idx_ = 0
    while ((d_4_idx_) < (len(numbers))):
        Invariant(Acc(list_pred(numbers)))
        Invariant(((0) <= (d_4_idx_)) and ((d_4_idx_) <= (len(numbers))))
        Invariant(not(res))
        Invariant(Forall(int, lambda d_5_i_:
            Implies((((0) <= (d_5_i_)) and ((d_5_i_) < (d_4_idx_))), 
            Forall(int, lambda d_6_j_:
                Implies((((0) <= (d_6_j_)) and ((d_6_j_) < (d_5_i_))), ((((numbers)[d_6_j_]) - ((numbers)[d_5_i_]) if (((numbers)[d_5_i_]) - ((numbers)[d_6_j_])) < (0) else ((numbers)[d_5_i_]) - ((numbers)[d_6_j_]))) >= (threshold))))))
        d_7_idx2_ = int(0) # type : int
        d_7_idx2_ = 0
        while ((d_7_idx2_) < (d_4_idx_)):
            Invariant(Acc(list_pred(numbers)))
            Invariant(((0) <= (d_4_idx_)) and ((d_4_idx_) < (len(numbers))))
            Invariant(((0) <= (d_7_idx2_)) and ((d_7_idx2_) <= (d_4_idx_)))
            Invariant(not(res))
            Invariant(Forall(int, lambda d_8_j_:
                Implies(0 <= d_8_j_ and d_8_j_ < d_7_idx2_, ((((numbers)[d_8_j_]) - ((numbers)[d_4_idx_]) if (((numbers)[d_4_idx_]) - ((numbers)[d_8_j_])) < (0) else ((numbers)[d_4_idx_]) - ((numbers)[d_8_j_]))) >= (threshold))))
            d_9_distance_ = 0 # type : int
            d_9_distance_ = (((numbers)[d_4_idx_]) - ((numbers)[d_7_idx2_]) if (((numbers)[d_7_idx2_]) - ((numbers)[d_4_idx_])) < (0) else ((numbers)[d_7_idx2_]) - ((numbers)[d_4_idx_]))
            if (d_9_distance_) < (threshold):
                res = True
                return res
            d_7_idx2_ = (d_7_idx2_) + (1)
        d_4_idx_ = (d_4_idx_) + (1)
    return res

