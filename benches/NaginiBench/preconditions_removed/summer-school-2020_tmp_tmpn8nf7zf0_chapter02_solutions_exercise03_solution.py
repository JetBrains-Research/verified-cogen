from typing import List, Tuple

from nagini_contracts.contracts import *


@Pure
def IsSorted(s : List[int]) -> bool :
    return Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < ((len(s)) - (1))), ((s)[d_0_i_]) <= ((s)[(d_0_i_) + (1)])))

def merge(a : List[int], b : List[int]) -> List[int]:
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
        Invariant(Acc(list_pred(output)))
        Invariant(Acc(list_pred(output1)))
        Invariant(Acc(list_pred(b)))
        Invariant(Acc(list_pred(a)))
        Invariant(((0) <= (d_6_ai_)) and ((d_6_ai_) <= (len(a))))
        Invariant(((0) <= (d_7_bi_)) and ((d_7_bi_) <= (len(b))))
        Invariant(Implies(len(output) > 0, len(output) == len(output1) + 1))
        Invariant(len(output) == d_6_ai_ + d_7_bi_)
        Invariant(IsSorted(a))
        Invariant(IsSorted(b))
        Invariant(Implies(len(output) > 0, Forall(int, lambda i : Implies(i >= 0 and i < len(output1), output[i] == output1[i]))))
        Invariant(Implies(((0) < (len(output))) and ((d_6_ai_) < (len(a))), ((output)[(len(output)) - (1)]) <= ((a)[d_6_ai_])))
        Invariant(Implies(((0) < (len(output))) and ((d_7_bi_) < (len(b))), ((output)[(len(output)) - (1)]) <= ((b)[d_7_bi_])))
        Invariant(Forall(int, lambda d_8_i_:
            Implies(((0) <= (d_8_i_)) and ((d_8_i_) < ((len(output)) - (1))), ((output)[d_8_i_]) <= ((output)[(d_8_i_) + (1)]))))
        output1 = list(output) # type : List[int]
        if ((d_6_ai_) == (len(a))) or (((d_7_bi_) < (len(b))) and (((a)[d_6_ai_]) > ((b)[d_7_bi_]))):
            output = (output) + [(b)[d_7_bi_]]
            d_7_bi_ = (d_7_bi_) + (1)
        else:
            output = (output) + [(a)[d_6_ai_]]
            d_6_ai_ = (d_6_ai_) + (1)
    return output