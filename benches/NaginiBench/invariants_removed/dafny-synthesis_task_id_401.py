from typing import Any, List, Tuple

from nagini_contracts.contracts import *


def IndexWiseAddition(a : List[List[int]], b : List[List[int]]) -> List[List[int]]:
    Requires(Acc(list_pred(b)))
    Requires(Forall(b, lambda b0: Acc(list_pred(b0))))
    Requires(Acc(list_pred(a)))
    Requires(Forall(a, lambda a0: Acc(list_pred(a0))))
    Requires(((len(a)) > (0)) and ((len(b)) > (0)))
    Requires((len(a)) == (len(b)))
    Requires(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(a))), (len((a)[d_0_i_])) == (len((b)[d_0_i_])))))
    Ensures(Acc(list_pred(b)))
    Ensures(Forall(b, lambda b0: Acc(list_pred(b0))))
    Ensures(Acc(list_pred(a)))
    Ensures(Forall(a, lambda a0: Acc(list_pred(a0))))
    Ensures(Acc(list_pred(Result())))
    Ensures((len(Result())) == (len(a)))
    Ensures((len(a)) == (len(b)))
    Ensures(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(a))), (len((a)[d_0_i_])) == (len((b)[d_0_i_])))))
    Ensures(Forall(int, lambda a0:  Implies(a0 >= 0 and a0 < len(Result()), Acc(list_pred(Result()[a0])))))
    Ensures(Forall(int, lambda d_1_i_:
        Implies(((0) <= (d_1_i_)) and ((d_1_i_) < (len(Result()))), (len((Result())[d_1_i_])) == (len((a)[d_1_i_])))))
    Ensures(Forall(int, lambda d_2_i_:
        Implies(((0) <= (d_2_i_)) and ((d_2_i_) < (len(Result()))), Forall(int, lambda d_3_j_:
            Implies(((0) <= (d_3_j_)) and ((d_3_j_) < (len((Result())[d_2_i_]))), (((Result())[d_2_i_])[d_3_j_]) == ((((a)[d_2_i_])[d_3_j_]) + (((b)[d_2_i_])[d_3_j_])))))))
    result = [[int(0)]] * 0 # type : List[List[int]]
    d_4_i_ = 0 # type : int
    while d_4_i_ < len(a):
        d_5_subResult_ = [int(0)] * 0 # type : List[int]
        d_6_j_ = 0 # type : int
        while d_6_j_ < len((a)[d_4_i_]):
            d_5_subResult_ = (d_5_subResult_) + [a[d_4_i_][d_6_j_] + b[d_4_i_][d_6_j_]]
            d_6_j_ = d_6_j_ + 1
        result = (result) + [d_5_subResult_]
        d_4_i_ = d_4_i_ + 1
    return result