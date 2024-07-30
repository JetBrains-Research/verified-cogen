from typing import List, Tuple
from nagini_contracts.contracts import *

@Pure
def IsSorted(s : List[int]) -> bool :
    Requires(Acc(list_pred(s)))
    return Forall(int, lambda i:
        (Implies(i >= 0 and i < len(s),
             Forall(int, lambda  j:
                (Implies(j > i and j < len(s), s[i] <= s[j]),
             [[s[j]]]))),
        [[s[i]]]))

def merge(a : List[int], b : List[int]) -> List[int]:
    Requires(Acc(list_pred(b)))
    Requires(Acc(list_pred(a)))
    Requires(IsSorted(a))
    Requires(IsSorted(b))
    Ensures(Acc(list_pred(b)))
    Ensures(Acc(list_pred(a)))
    Ensures(Acc(list_pred(Result())))
    Ensures(IsSorted(Result()))
    Ensures(len(Result()) == len(a) + len(b))
    output = list([int(0)] * 0) # type : List[int]
    d_6_ai_ = int(0) # type : int
    d_6_ai_ = 0
    d_7_bi_ = int(0) # type : int
    d_7_bi_ = 0
    while ((d_6_ai_) < (len(a))) or ((d_7_bi_) < (len(b))):
        if ((d_6_ai_) == (len(a))) or (((d_7_bi_) < (len(b))) and (((a)[d_6_ai_]) > ((b)[d_7_bi_]))):
            output_prev = output
            output = (output) + [(b)[d_7_bi_]]
            d_7_bi_ = (d_7_bi_) + (1)
        else:
            output_prev = output
            output = (output) + [(a)[d_6_ai_]]
            d_6_ai_ = (d_6_ai_) + (1)
    return output