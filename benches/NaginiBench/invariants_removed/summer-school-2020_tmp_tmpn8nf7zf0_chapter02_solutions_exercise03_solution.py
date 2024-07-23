from typing import List, Tuple

from nagini_contracts.contracts import *


@Pure
def IsSorted(s : List[int]) -> bool :
    Requires(Acc(list_pred(s)))
    return Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < ((len(s)) - (1))), ((s)[d_0_i_]) <= ((s)[(d_0_i_) + (1)])))

def merge(a : List[int], b : List[int]) -> List[int]:
    Requires(Acc(list_pred(b)))
    Requires(Acc(list_pred(a)))
    Requires(IsSorted(a))
    Requires(IsSorted(b))
    Ensures(Acc(list_pred(b)))
    Ensures(Acc(list_pred(a)))
    Ensures(Acc(list_pred(Result())))
    Ensures(IsSorted(Result()))
    output = list([int(0)] * 0) # type : List[int]
    d_6_ai_ = int(0) # type : int
    d_6_ai_ = 0
    d_7_bi_ = int(0) # type : int
    d_7_bi_ = 0
    output1 = list(output) # type : List[int]
    while ((d_6_ai_) < (len(a))) or ((d_7_bi_) < (len(b))):
        output1 = list(output) # type : List[int]
        if ((d_6_ai_) == (len(a))) or (((d_7_bi_) < (len(b))) and (((a)[d_6_ai_]) > ((b)[d_7_bi_]))):
            output = (output) + [(b)[d_7_bi_]]
            d_7_bi_ = (d_7_bi_) + (1)
        else:
            output = (output) + [(a)[d_6_ai_]]
            d_6_ai_ = (d_6_ai_) + (1)
    return output