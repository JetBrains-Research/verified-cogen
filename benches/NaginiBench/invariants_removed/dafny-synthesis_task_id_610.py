from typing import List, Tuple
from nagini_contracts.contracts import *

def RemoveElement(s : List[int], k : int) -> List[int]:
    Requires(Acc(list_pred(s)))
    Requires(((0) <= (k)) and ((k) < (len((s)))))
    Ensures(Acc(list_pred(s)))
    Ensures(Acc(list_pred(Result())))
    Ensures((len((Result()))) == ((len((s))) - (1)))
    Ensures(((0) <= (k)) and ((k) < (len((s)))))
    Ensures(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (k)), ((Result())[d_0_i_]) == ((s)[d_0_i_]))))
    Ensures(Forall(int, lambda d_1_i_:
        Implies(((k) <= (d_1_i_)) and ((d_1_i_) < (len((Result())))), ((Result())[d_1_i_]) == ((s)[(d_1_i_) + (1)]))))
    v = [int(0)] * 0 # type : List[int]
    nw0_ = [int(0)] * ((len((s))) - (1)) # type : List[int]
    v = nw0_
    d_2_i_ = int(0) # type : int
    d_2_i_ = 0
    while (d_2_i_) < (k):
        (v)[(d_2_i_)] = (s)[d_2_i_]
        d_2_i_ = (d_2_i_) + (1)
    while (d_2_i_) < (len((v))):
        (v)[(d_2_i_)] = (s)[(d_2_i_) + (1)]
        d_2_i_ = (d_2_i_) + (1)
    return v