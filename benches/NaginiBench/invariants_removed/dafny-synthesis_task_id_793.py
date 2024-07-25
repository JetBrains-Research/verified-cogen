from typing import List, Tuple
from nagini_contracts.contracts import *

def LastPosition(arr : List[int], elem : int) -> int:
    Requires(Acc(list_pred(arr)))
    Requires((len((arr))) > (0))
    Requires(Forall(int, lambda d_0_i_:
        Forall(int, lambda d_1_j_:
            Implies((((0) <= (d_0_i_)) and ((d_0_i_) < (d_1_j_))) and ((d_1_j_) < (len((arr)))), ((arr)[d_0_i_]) <= ((arr)[d_1_j_])))))
    Ensures(Acc(list_pred(arr)))
    Ensures(len(arr) == len(Old(arr)))
    Ensures(((Result()) == (-1)) or (((((0) <= (Result())) and ((Result()) < (len((arr))))) and (((arr)[Result()]) == (elem))) and (((Result()) == ((len((arr))) - (1))) or (((arr)[(Result()) + (1)]) > (elem)))))
    Ensures(Forall(int, lambda d_2_i_:
        Implies(((0) <= (d_2_i_)) and ((d_2_i_) < (len((arr)))), ((arr)[d_2_i_]) == (Old(arr)[d_2_i_]))))
    pos = int(0) # type : int
    pos = -1
    d_3_i_ = 0 # type : int
    while d_3_i_ < len(arr):
        if ((arr)[d_3_i_]) == (elem):
            pos = d_3_i_
        d_3_i_ = d_3_i_ + 1
    return pos
