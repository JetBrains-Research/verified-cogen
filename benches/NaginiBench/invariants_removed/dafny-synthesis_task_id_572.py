from typing import List, Tuple
from nagini_contracts.contracts import *

@Pure
def InArray(a : List[int], x : int) -> bool :
    Requires(Acc(list_pred(a)))
    return Exists(int, lambda d_0_i_:
        ((((0) <= (d_0_i_)) and ((d_0_i_) < (len((a))))) and (((a)[d_0_i_]) == (x))))

@Pure
def NotInArray(a : List[int], x : int) -> bool :
    Requires(Acc(list_pred(a)))
    return Forall(int, lambda d_0_i_:
        (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len((a)))), ((a)[d_0_i_]) != (x)), [[(a)[d_0_i_]]]))


def RemoveDuplicates(a : List[int]) -> List[int]:
    Requires(Acc(list_pred(a)))
    Ensures(Acc(list_pred(a)))
    Ensures(Acc(list_pred(Result())))
    Ensures(Forall(int, lambda d_6_x_:
        Implies(d_6_x_ >= 0 and d_6_x_ < len(Result()), (InArray(a, Result()[d_6_x_])))))
    Ensures(Forall(int, lambda d_2_i_:
        Forall(int, lambda d_3_j_:
            Implies ((((0) <= (d_2_i_)) and ((d_2_i_) < (d_3_j_))) and ((d_3_j_) < (len(Result()))), ((Result())[d_2_i_]) != ((Result())[d_3_j_])))))
    result = list([int(0)] * 0) # type : List[int]
    d_4_res_ = list([int(0)] * 0) # type : List[int]
    d_4_res_ = list([])
    d_5_i_ = int(0)
    while d_5_i_ < len(a):
        if (NotInArray(d_4_res_, (a)[d_5_i_])):
            d_4_res_prev = list(d_4_res_)
            d_4_res_ = (d_4_res_) + ([(a)[d_5_i_]])
        d_5_i_ = d_5_i_ + 1
    result = d_4_res_
    return result