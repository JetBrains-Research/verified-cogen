from typing import Dict, List, Optional, Set, Union, cast

from nagini_contracts.contracts import *


def has__close__elements(numbers : List[int], threshold : int) -> bool:
    Requires(Acc(list_pred(numbers)))
    Requires((threshold) >= (0))
    Ensures(Acc(list_pred(numbers)))
    Ensures(not (not(Result())) or (Forall(int, lambda d_2_i_:
        Forall(int, lambda d_3_j_:
            Implies((((1) <= (d_2_i_)) and ((d_2_i_) < (len(numbers)))) and (((0) <= (d_3_j_)) and ((d_3_j_) < (d_2_i_))), ((((numbers)[d_3_j_]) - ((numbers)[d_2_i_]) if (((numbers)[d_2_i_]) - ((numbers)[d_3_j_])) < (0) else ((numbers)[d_2_i_]) - ((numbers)[d_3_j_]))) >= (threshold))))))
    res = False # type : bool
    res = False
    d_4_idx_ = int(0) # type : int
    d_4_idx_ = 0
    while ((d_4_idx_) < (len(numbers))):
        d_7_idx2_ = int(0) # type : int
        d_7_idx2_ = 0
        while ((d_7_idx2_) < (d_4_idx_)):
            d_9_distance_ = 0 # type : int
            d_9_distance_ = (((numbers)[d_4_idx_]) - ((numbers)[d_7_idx2_]) if (((numbers)[d_7_idx2_]) - ((numbers)[d_4_idx_])) < (0) else ((numbers)[d_7_idx2_]) - ((numbers)[d_4_idx_]))
            if (d_9_distance_) < (threshold):
                res = True
                return res
            d_7_idx2_ = (d_7_idx2_) + (1)
        d_4_idx_ = (d_4_idx_) + (1)
    return res

