from typing import List, Tuple
from nagini_contracts.contracts import *

def HasOnlyOneDistinctElement(a : List[int]) -> bool:
    Requires(Acc(list_pred(a)))
    Ensures(Acc(list_pred(a)))
    Ensures(Implies(Result(), Forall(int, lambda d_0_i_:
        Forall(int, lambda d_1_j_:
            Implies((((0) <= (d_0_i_)) and ((d_0_i_) < (len((a))))) and (((0) <= (d_1_j_)) and ((d_1_j_) < (len((a))))), ((a)[d_0_i_]) == ((a)[d_1_j_]))))))
    Ensures(Implies(not(Result()), Exists(int, lambda d_2_i_:
        Exists(int, lambda d_3_j_:
            ((((0) <= (d_2_i_)) and ((d_2_i_) < (len((a))))) and (((0) <= (d_3_j_)) and ((d_3_j_) < (len((a)))))) and (((a)[d_2_i_]) != ((a)[d_3_j_]))))))
    result = False # type : bool
    if (len((a))) == (0):
        result = True
        return result
    d_4_firstElement_ = int(0) # type : int
    d_4_firstElement_ = (a)[0]
    result = True
    d_5_i_ = int(1) # type : int
    while d_5_i_ < len(a):
        if ((a)[d_5_i_]) != (d_4_firstElement_):
            result = False
            break
        d_5_i_ = d_5_i_ + 1
    return result