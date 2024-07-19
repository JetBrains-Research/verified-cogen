from typing import List, Tuple
from nagini_contracts.contracts import *

@Pure
def InArray(a : List[int], x : int) -> bool :
    Requires(Acc(list_pred(a)))
    return Exists(int, lambda d_0_i_:
        (((0) <= (d_0_i_)) and ((d_0_i_) < (len((a))))) and (((a)[d_0_i_]) == (x)))

def partition(a : List[int]) -> int:
    Requires(Acc(list_pred(a)))
    Requires((len((a))) > (0))
    Ensures(Acc(list_pred(a)))
    Ensures(((0) <= (Result())) and ((Result()) < (len((a)))))
    Ensures(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (Result())), ((a)[d_0_i_]) < ((a)[Result()]))))
    Ensures(Forall(int, lambda d_1_i_:
        Implies(((Result()) < (d_1_i_)) and ((d_1_i_) < (len((a)))), ((a)[d_1_i_]) >= ((a)[Result()]))))
    Ensures(Forall(int, lambda d_6_x_:
        Implies(d_6_x_ >= 0 and d_6_x_ < len(a), (InArray(Old(a), a[d_6_x_])))))
    # Ensures((_dafny.MultiSet(list((a)[::]))) == (_dafny.MultiSet(Old(list((a)[::])))))
    pivotPos = int(0) # type : int
    pivotPos = (len((a))) - (1)
    d_2_i_ = int(0) # type : int
    d_2_i_ = 0
    d_3_j_ = int(0) # type : int
    d_3_j_ = 0
    d_2_i_shadow = 0
    a_shadow = [int(0)] * len(a) # type : List[int]
    while (d_3_j_) < ((len((a))) - (1)):
        Invariant(Acc(list_pred(a)))
        Invariant(Acc(list_pred(a_shadow)))
        Invariant(len(a) == len(a_shadow))
        Invariant((((0) <= (d_2_i_)) and ((d_2_i_) <= (d_3_j_))) and ((d_3_j_) < (len((a)))))
        Invariant(pivotPos == len(a) - 1)
        Invariant(d_3_j_ <= pivotPos)
        Invariant(d_2_i_ <= pivotPos)
        Invariant((len((a))) > (0))
        Invariant(len(a) == Old(len(a)))
        Invariant(Forall(int, lambda d_4_k_:
            Implies(((0) <= (d_4_k_)) and ((d_4_k_) < (d_2_i_)), ((a)[d_4_k_]) < ((a)[pivotPos]))))
        Invariant(Forall(int, lambda d_5_k_:
            Implies(((d_2_i_) <= (d_5_k_)) and ((d_5_k_) < (d_3_j_)), ((a)[d_5_k_]) >= ((a)[pivotPos]))))
        Invariant(Implies(Old(d_2_i_) != d_2_i_, Forall(int, lambda d_6_x_:
            Implies(d_6_x_ >= 0 and d_6_x_ < len(a), (InArray(Old(a), a[d_6_x_]))))))
        Invariant(Implies(Old(d_2_i_) != d_2_i_, Forall(int, lambda d_6_x_:
            Implies(d_6_x_ >= 0 and d_6_x_ < len(a), (InArray(a, Old(a)[d_6_x_]))))))
        Invariant(Implies(d_3_j_ > 0, Implies(d_2_i_shadow == d_2_i_, Forall(int, lambda d_6_x_:
            Implies(d_6_x_ >= 0 and d_6_x_ < len(a), (InArray(a, a_shadow[d_6_x_]))))))) # ??
        # Invariant(Implies(Old(d_2_i_) == d_2_i_, Forall(int, lambda d_6_x_:
        #     Implies(d_6_x_ >= 0 and d_6_x_ < len(a), (InArray(a, Old(a)[d_6_x_])))))) # ??
        # Invariant(pivotPos == Old(pivotPos))
        # Invariant(Implies(d_3_j_ > 0, Implies((d_2_i_) == Old(d_2_i_) + 1, (Old(a)[Old(d_3_j_)]) < (Old(a)[pivotPos]))))
        # Invariant(Implies(d_3_j_ > 0, Implies((Old(a[d_3_j_ - 1])) >= (Old(a[pivotPos])), (d_2_i_) == Old(d_2_i_))))
        # # Invariant(Implies(d_3_j_ > 0, Implies((d_2_i_) == Old(d_2_i_), (Old(a[Old(d_3_j_)])) >= (Old(a[pivotPos])))))
        # Invariant(Implies(Old(d_2_i_) == d_2_i_, Forall(int, lambda i: Implies(i >= d_3_j_ and i < len(a), a[i] == Old(a[i])))))
        # Invariant(Implies(Old(d_2_i_) == d_2_i_, a[d_2_i_] == Old(a[d_2_i_])))
        # Invariant(Implies(Old(d_2_i_) == d_2_i_, Forall(int, lambda i: Implies(i > d_2_i_ and i < len(a), a[i] == Old(a[i])))))
        # Invariant(d_2_i_ == Old(d_2_i_) + 1 or d_2_i_ == Old(d_2_i_))
        # Invariant(Implies(Old(d_2_i_) == d_2_i_, Forall(int, lambda i: Implies(i >= 0 and i < Old(d_2_i_), a[i] == Old(a[i])))))
        # Invariant(Implies(Old(d_2_i_) == d_2_i_, Forall(int, lambda i: Implies(i >= 0 and i < len(a), a[i] == Old(a[i])))))
        # Invariant(Forall(int, lambda d_6_x_:
        #     Implies(d_6_x_ >= 0 and d_6_x_ < len(a), (InArray(Old(a), a[d_6_x_])))))
        # Invariant((_dafny.MultiSet(list((a)[::]))) == (_dafny.MultiSet(Old(list((a)[::])))))
        #decreases a.Length - 1 - j
        d_2_i_shadow = d_2_i_
        a_shadow = list(a)
        if ((a)[d_3_j_]) < ((a)[pivotPos]):
            rhs0_ = (a)[d_3_j_] # type : int
            a[d_3_j_] = a[d_2_i_]
            a[d_2_i_] = rhs0_
            d_2_i_ = d_2_i_ + 1
            Assert(d_2_i_ == d_2_i_shadow + 1)
            Assert(Forall(int, lambda d_6_x_: Implies(d_6_x_ >= 0 and d_6_x_ < len(a), (InArray(a, a_shadow[d_6_x_])))))
            Assert(Forall(int, lambda d_6_x_: Implies(d_6_x_ >= 0 and d_6_x_ < len(a), (InArray(a_shadow, a[d_6_x_])))))
        elif ((a)[d_3_j_]) >= ((a)[pivotPos]):
            Assert(Forall(int, lambda d_6_x_: Implies(d_6_x_ >= 0 and d_6_x_ < len(a), (InArray(a, a_shadow[d_6_x_])))))
            Assert(Forall(int, lambda d_6_x_: Implies(d_6_x_ >= 0 and d_6_x_ < len(a), (InArray(a_shadow, a[d_6_x_])))))
            d_2_i_ = d_2_i_
            Assert(d_2_i_ == d_2_i_shadow)
        Assert(Implies(d_2_i_shadow == d_2_i_, Forall(int, lambda d_6_x_:
            Implies(d_6_x_ >= 0 and d_6_x_ < len(a), (InArray(a, a_shadow[d_6_x_])))))) # ??
        d_3_j_ = d_3_j_ + 1
    rhs2_ = (a)[d_2_i_] # type : int
    a[d_2_i_] = a[(len((a))) - (1)]
    (a)[(len((a))) - (1)] = rhs2_
    pivotPos = d_2_i_
    return pivotPos