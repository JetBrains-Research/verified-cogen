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
        Invariant(Acc(list_pred(output)))
        Invariant(Acc(list_pred(b)))
        Invariant(Acc(list_pred(a)))
        Invariant(((0) <= (d_6_ai_)) and ((d_6_ai_) <= (len(a))))
        Invariant(((0) <= (d_7_bi_)) and ((d_7_bi_) <= (len(b))))
        Invariant(len(output) == d_6_ai_ + d_7_bi_)
        Invariant(IsSorted(a))
        Invariant(IsSorted(b))
        Invariant(Implies(((0) < (len(output))) and ((d_6_ai_) < (len(a))), ((output)[(len(output)) - (1)]) <= ((a)[d_6_ai_])))
        Invariant(Implies(((0) < (len(output))) and ((d_7_bi_) < (len(b))), ((output)[(len(output)) - (1)]) <= ((b)[d_7_bi_])))
        Invariant(IsSorted(output))
        Invariant(Implies(((0) < (len(output))) and ((d_6_ai_) < (len(a))),
          Forall(int, lambda j:
            (Implies(j >= 0 and j < len(output), output[j] <= a[d_6_ai_]), [[output[j]]]))))
        Invariant(Implies(((0) < (len(output))) and ((d_7_bi_) < (len(b))),
          Forall(int, lambda j:
            (Implies(j >= 0 and j < len(output), output[j] <= b[d_7_bi_]), [[output[j]]]))))
        if ((d_6_ai_) == (len(a))) or (((d_7_bi_) < (len(b))) and (((a)[d_6_ai_]) > ((b)[d_7_bi_]))):
            output_prev = output
            Assert(Forall(int, lambda i:
                (Implies(i >= 0 and i < len(output),
                    Forall(int, lambda j:
                        (Implies(j > i and j < len(output), output[i] <= output[j]),
                    [[output_prev[j]]]))),
                [[output_prev[i]]])))
            output = (output) + [(b)[d_7_bi_]]
            d_7_bi_ = (d_7_bi_) + (1)
        else:
            output_prev = output
            Assert(Forall(int, lambda i:
                (Implies(i >= 0 and i < len(output),
                    Forall(int, lambda j:
                        (Implies(j > i and j < len(output), output[i] <= output[j]),
                    [[output_prev[j]]]))),
                [[output_prev[i]]])))
            output = (output) + [(a)[d_6_ai_]]
            d_6_ai_ = (d_6_ai_) + (1)
    return output