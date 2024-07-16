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
        Implies(((0) <= (d_2_i_)) and ((d_2_i_) < (len((arr)))), ((arr)[d_2_i_]) == (Old((arr)[d_2_i_])))))
    pos = int(0) # type : int
    pos = -1
    hi0_ = len((arr)) # type : int
    for d_3_i_ in range(0, hi0_):
        Invariant(Acc(list_pred(arr)))
        Invariant(((0) <= (d_3_i_)) and ((d_3_i_) <= (len((arr)))))
        Invariant(((pos) == (-1)) or (((((0) <= (pos)) and ((pos) < (d_3_i_))) and (((arr)[pos]) == (elem))) and (((pos) == ((d_3_i_) - (1))) or (((arr)[(pos) + (1)]) > (elem)))))
        Invariant(Forall(int, lambda d_4_k_:
            Implies(((0) <= (d_4_k_)) and ((d_4_k_) < (len((arr)))), ((arr)[d_4_k_]) == (Old((arr)[d_4_k_])))))
        if ((arr)[d_3_i_]) == (elem):
            pos = d_3_i_
    return pos
