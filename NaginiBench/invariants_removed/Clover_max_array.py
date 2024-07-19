from typing import List
from nagini_contracts.contracts import *

def maxArray(a : List[int]) -> int:
    Requires(Acc(list_pred(a)))
    Requires((len((a))) >= (1))
    Ensures(Acc(list_pred(a)))
    Ensures(Forall(int, lambda d_0_k_:
        Implies(((0) <= (d_0_k_)) and ((d_0_k_) < (len((a)))), (Result()) >= ((a)[d_0_k_]))))
    Ensures(Exists(int, lambda d_1_k_:
        (((0) <= (d_1_k_)) and ((d_1_k_) < (len((a))))) and ((Result()) == ((a)[d_1_k_]))))
    m = int(0) # type : int
    m = (a)[0]
    d_2_index_ = int(0) # type : int
    d_2_index_ = 1
    while (d_2_index_) < (len((a))):
        m = (m if (m) > ((a)[d_2_index_]) else (a)[d_2_index_])
        d_2_index_ = (d_2_index_) + (1)
    return m

