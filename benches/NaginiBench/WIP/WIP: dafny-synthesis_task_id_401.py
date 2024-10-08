from typing import List, Tuple, Any
from nagini_contracts.contracts import *


def IndexWiseAddition(a : List[List[int]], b : List[List[int]]) -> List[List[int]]:
    Requires(Acc(list_pred(b)))
    # Requires(Forall(int, lambda d_0_i_:
    #     Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(b))), Acc(list_pred(b[d_0_i_])))))
    Requires(Forall(b, lambda d_0_i_:
        Acc(list_pred(d_0_i_))))
    Requires(Acc(list_pred(a)))
    Requires(Forall(a, lambda d_0_i_:
        (Acc(list_pred(d_0_i_)), [[d_0_i_]])))
    Requires(((len(a)) > (0)) and ((len(b)) > (0)))
    Requires((len(a)) == (len(b)))
    Requires(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(a))), (len((a)[d_0_i_])) == (len((b)[d_0_i_])))))
    Ensures(Acc(list_pred(b)))
    Ensures(Forall(b, lambda d_0_i_:
        (Acc(list_pred(d_0_i_)))))
    # Ensures(Forall(int, lambda d_0_i_:
    #     (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(b))), Acc(list_pred(b[d_0_i_]))), [[b[d_0_i_]]])))
    # Ensures(Forall(b, lambda b0: Acc(list_pred(b0))))
    Ensures(Acc(list_pred(a)))
    Ensures(Forall(a, lambda d_0_i_:
        (Acc(list_pred(d_0_i_)))))
    # Ensures(Forall(int, lambda d_0_i_:
    #     (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(a))), Acc(list_pred(a[d_0_i_]))), [[a[d_0_i_]]])))
    # Ensures(Forall(a, lambda a0: Acc(list_pred(a0))))
    Ensures(Acc(list_pred(Result())))
    # Ensures(Forall(int, lambda d_0_i_:
    #     (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(Result()))), Acc(list_pred(Result()[d_0_i_]))), [[Result()[d_0_i_]]])))
    Ensures((len(Result())) == (len(a)))
    Ensures((len(a)) == (len(b)))
    Ensures(Forall(int, lambda d_0_i_:
        Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(a))), (len((a)[d_0_i_])) == (len((b)[d_0_i_])))))
    # Ensures(Forall(int, lambda a0:  Implies(a0 >= 0 and a0 < len(Result()), Acc(list_pred(Result()[a0])))))
    # Ensures(Forall(int, lambda d_1_i_:
    #     Implies(((0) <= (d_1_i_)) and ((d_1_i_) < (len(Result()))), (len((Result())[d_1_i_])) == (len((a)[d_1_i_])))))
    # Ensures(Forall(int, lambda d_2_i_:
    #     Implies(((0) <= (d_2_i_)) and ((d_2_i_) < (len(Result()))), Forall(int, lambda d_3_j_:
    #         Implies(((0) <= (d_3_j_)) and ((d_3_j_) < (len((Result())[d_2_i_]))), (((Result())[d_2_i_])[d_3_j_]) == ((((a)[d_2_i_])[d_3_j_]) + (((b)[d_2_i_])[d_3_j_])))))))
    result = [[int(0)]] * 0 # type : List[List[int]]
    d_4_i_ = 0 # type : int
    while d_4_i_ < len(a):
        Invariant(Acc(list_pred(result)))
        Invariant(Forall(result, lambda d_0_i_:
            (Acc(list_pred(d_0_i_)))))
        # Invariant(Forall(int, lambda d_0_i_:
        #     (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(result))), Acc(list_pred(result[d_0_i_]))), [[result[d_0_i_]]])))
        # Invariant(Forall(result, lambda r0: Acc(list_pred(r0))))
        Invariant(Acc(list_pred(b)))
        Invariant(Forall(b, lambda d_0_i_:
            (Acc(list_pred(d_0_i_)))))
        # Invariant(Forall(int, lambda d_0_i_:
        #     (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(b))), Acc(list_pred(b[d_0_i_]))), [[b[d_0_i_]]])))
        # Invariant(Forall(b, lambda b0: Acc(list_pred(b0))))
        Invariant(Acc(list_pred(a)))
        Invariant(Forall(a, lambda d_0_i_:
            (Acc(list_pred(d_0_i_)))))
        # Invariant(Forall(int, lambda d_0_i_:
        #     (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(a))), Acc(list_pred(a[d_0_i_]))), [[a[d_0_i_]]])))
        # Invariant(Forall(a, lambda a0: Acc(list_pred(a0))))
        Invariant(((0) <= (d_4_i_)) and ((d_4_i_) <= (len(a))))
        Invariant((len(result)) == (d_4_i_))
        Invariant((len(a)) == (len(b)))
        Invariant(Forall(int, lambda d_0_i_:
            (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(a))), (len((a)[d_0_i_])) == (len((b)[d_0_i_]))), [[b[d_0_i_]]])))
        Invariant(Forall(int, lambda d_1_i_:
            (Implies(((0) <= (d_1_i_)) and ((d_1_i_) < (len(result))), (len((result)[d_1_i_])) == (len((a)[d_1_i_]))), [[(result)[d_1_i_]]])))
        Invariant(Forall(int, lambda d_9_k_:
            (Implies(((0) <= (d_9_k_)) and ((d_9_k_) < (d_4_i_)),
                Forall(int, lambda d_10_j_:
                    (Implies(((0) <= (d_10_j_)) and ((d_10_j_) < (len((result)[d_9_k_]))), (((result)[d_9_k_])[d_10_j_]) == ((((a)[d_9_k_])[d_10_j_]) + (((b)[d_9_k_])[d_10_j_]))),
                        [[((result)[d_9_k_])[d_10_j_]]]))),
                [[(result)[d_9_k_]]])))
        d_5_subResult_ = [int(0)] * 0 # type : List[int]
        d_6_j_ = 0 # type : int
        while d_6_j_ < len((a)[d_4_i_]):
            Invariant(Acc(list_pred(d_5_subResult_)))
            Invariant(Acc(list_pred(result)))
            Invariant(Forall(result, lambda d_0_i_:
                (Acc(list_pred(d_0_i_)))))
            # Invariant(Forall(int, lambda d_0_i_:
            #     (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(result))), Acc(list_pred(result[d_0_i_]))), [[result[d_0_i_]]])))
            # Invariant(Forall(result, lambda r0: Acc(list_pred(r0))))
            Invariant(Acc(list_pred(b)))
            Invariant(Forall(b, lambda d_0_i_:
                (Acc(list_pred(d_0_i_)))))
            # Invariant(Forall(int, lambda d_0_i_:
            #     (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(b))), Acc(list_pred(b[d_0_i_]))), [[b[d_0_i_]]])))
            # Invariant(Forall(b, lambda b0: Acc(list_pred(b0))))
            Invariant(Acc(list_pred(a)))
            Invariant(Forall(a, lambda d_0_i_:
                (Acc(list_pred(d_0_i_)))))
            # Invariant(Forall(int, lambda d_0_i_:
            #     (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(a))), Acc(list_pred(a[d_0_i_]))), [[a[d_0_i_]]])))
            # Invariant(Forall(a, lambda a0: Acc(list_pred(a0))))
            Invariant(((0) <= (d_4_i_)) and ((d_4_i_) < (len(a))))
            Invariant(((0) <= (d_6_j_)) and ((d_6_j_) <= (len((a)[d_4_i_]))))
            Invariant((len(d_5_subResult_)) == (d_6_j_))
            Invariant((len(result)) == (d_4_i_))
            Invariant((len(a)) == (len(b)))
            Invariant(Forall(int, lambda d_0_i_:
                (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(a))), (len((a)[d_0_i_])) == (len((b)[d_0_i_]))), [[b[d_0_i_]]])))
            Invariant(Forall(int, lambda d_1_i_:
                (Implies(((0) <= (d_1_i_)) and ((d_1_i_) < (len(result))), (len((result)[d_1_i_])) == (len((a)[d_1_i_]))), [[(result)[d_1_i_]]])))
            Invariant(Forall(int, lambda d_9_k_:
                (Implies(((0) <= (d_9_k_)) and ((d_9_k_) < (d_4_i_)),
                    Forall(int, lambda d_10_j_:
                        (Implies(((0) <= (d_10_j_)) and ((d_10_j_) < (len((result)[d_9_k_]))), (((result)[d_9_k_])[d_10_j_]) == ((((a)[d_9_k_])[d_10_j_]) + (((b)[d_9_k_])[d_10_j_]))),
                            [[((result)[d_9_k_])[d_10_j_]]]))),
                    [[(result)[d_9_k_]]])))
            Invariant(Forall(int, lambda d_7_k_:
                (Implies(((0) <= (d_7_k_)) and ((d_7_k_) < (d_6_j_)), ((d_5_subResult_)[d_7_k_]) == ((((a)[d_4_i_])[d_7_k_]) + (((b)[d_4_i_])[d_7_k_]))),
                    [[(d_5_subResult_)[d_7_k_]]])))
            d_5_subResult_prev = list(d_5_subResult_)
            Assert(Forall(int, lambda d_7_k_:
                (Implies(((0) <= (d_7_k_)) and ((d_7_k_) < (d_6_j_)), ((d_5_subResult_)[d_7_k_]) == ((((a)[d_4_i_])[d_7_k_]) + (((b)[d_4_i_])[d_7_k_]))),
                    [[(d_5_subResult_prev)[d_7_k_]]])))
            d_5_subResult_ = (d_5_subResult_) + [a[d_4_i_][d_6_j_] + b[d_4_i_][d_6_j_]]
            d_6_j_ = d_6_j_ + 1
        result_prev = list(result)
        Assert(Forall(int, lambda d_9_k_:
            (Implies(((0) <= (d_9_k_)) and ((d_9_k_) < (d_4_i_)),
                Forall(int, lambda d_10_j_:
                (Implies(((0) <= (d_10_j_)) and ((d_10_j_) < (len((result)[d_9_k_]))),
                    (((result)[d_9_k_])[d_10_j_]) == ((((a)[d_9_k_])[d_10_j_]) + (((b)[d_9_k_])[d_10_j_]))),
                [[((result_prev)[d_9_k_])[d_10_j_]]]))),
            [[(result_prev)[d_9_k_]]])))
        result = (result) + [d_5_subResult_]
        d_4_i_ = d_4_i_ + 1
    return result