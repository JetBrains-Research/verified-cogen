from typing import List, TypeVar, Type, Callable
from nagini_contracts.contracts import *

def insert(line : List[int], l : int, nl : List[int], p : int, at : int) -> None:
    Ensures(Acc(list_pred(nl)))
    Ensures(Acc(list_pred(line)))
    Ensures(p <= len(nl))
    Ensures(at <= l)
    Ensures(l + p <= len(line))
    Ensures(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (p)), ((line)[(at) + (d_0_i_)]) == ((nl)[d_0_i_]))))
    Ensures(Forall(int, lambda d_1_i_:
        Implies(((0) <= (d_1_i_)) and ((d_1_i_) < (at)), ((line)[d_1_i_]) == (Old((line)[d_1_i_])))))
    Ensures(Forall(int, lambda d_2_i_:
        Implies(((at) <= (d_2_i_)) and ((d_2_i_) < (l)), ((line)[(d_2_i_) + (p)]) == (Old((line)[d_2_i_])))))
    d_4_initialLine_ = list(line) # type : List[int]
    d_3_i_ = int(0) # type : int
    d_3_i_ = l
    while (d_3_i_) > (at):
        Invariant(Acc(list_pred(nl)))
        Invariant(Acc(list_pred(line)))
        Invariant(Acc(list_pred(d_4_initialLine_), 1/2))
        Invariant(d_3_i_ <= len(line))
        Invariant(d_3_i_ <= len(d_4_initialLine_))
        Invariant(l + p <= len(line))
        Invariant(l <= len(d_4_initialLine_))
        Invariant(d_3_i_ >= 0 and p >= 0)
        Invariant(p <= len(nl))
        Invariant(Forall(int, lambda i : (Implies(i >= 0 and i < d_3_i_, line[i] == d_4_initialLine_[i]), [[line[i]]])))
        Invariant(Forall(int, lambda i : (Implies(i >= d_3_i_ + p and i < l + p, ((line)[i]) == ((d_4_initialLine_)[i - p])), [[(line)[i]]])))
        Invariant(((at) <= (d_3_i_)) and ((d_3_i_) <= (l)))
        d_3_i_ = (d_3_i_) - (1)
        index0_ = (d_3_i_) + (p) # type : int
        (line)[index0_] = (line)[d_3_i_]
    d_3_i_ = 0
    while (d_3_i_) < (p):
        Invariant(Acc(list_pred(nl)))
        Invariant(Acc(list_pred(line)))
        Invariant(Acc(list_pred(d_4_initialLine_), 1/2))
        Invariant(((0) <= (d_3_i_)) and ((d_3_i_) <= (p)))
        Invariant(at <= len(line))
        Invariant(at <= len(d_4_initialLine_))
        Invariant(l + p <= len(line))
        Invariant(l <= len(d_4_initialLine_))
        Invariant(d_3_i_ >= 0 and p >= 0)
        Invariant(at + d_3_i_ <= len(line))
        Invariant(d_3_i_ <= len(nl))
        Invariant(p <= len(nl))
        Invariant(Forall(int, lambda i: (Implies(i >= 0 and i < at, (((line)[i])) == (((d_4_initialLine_)[i]))), [[(line)[i]]])))
        Invariant(Forall(int, lambda i: (Implies(i >= at and i < at + d_3_i_, (((line)[i])) == (((nl)[i - at]))), [[line[i]]])))
        Invariant(Forall(int, lambda i: (Implies(i >= at + p and i < l + p, (((line)[i])) == (((d_4_initialLine_)[i - p]))), [[(line)[i]]])))
        index1_ = (at) + (d_3_i_) # type : int
        (line)[index1_] = (nl)[d_3_i_]
        d_3_i_ = (d_3_i_) + (1)

