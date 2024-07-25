from typing import List, Tuple
from nagini_contracts.contracts import *

def twoSum(nums : List[int], target : int) -> Tuple[int, int]:
    Ensures(Acc(list_pred(nums)))
    Ensures((Result()[0]) != (Result()[1]))
    Ensures(((0) <= (Result()[0])) and ((Result()[0]) < (len((nums)))))
    Ensures(((0) <= (Result()[1])) and ((Result()[1]) < (len((nums)))))
    Ensures((((nums)[Result()[0]]) + ((nums)[Result()[1]])) == (target))
    d_2_i_ = int(0) # type : int
    while (d_2_i_) < (len((nums))):
        Invariant(Acc(list_pred(nums)))
        Invariant((2) <= (len((nums))))
        Invariant(((0) <= (d_2_i_)) and ((d_2_i_) < (len((nums)))))
        Invariant(Forall(int, lambda d_3_u_:
            (Forall(int, lambda d_4_v_:
                (Implies(((((0) <= (d_3_u_)) and ((d_3_u_) < (d_4_v_))) and ((d_4_v_) < (len((nums))))) and ((d_3_u_) < (d_2_i_)), (((nums)[d_3_u_]) + ((nums)[d_4_v_])) != (target)),
                    [[(nums)[d_4_v_]]])),
                [[(nums)[d_3_u_]]])))
        Invariant(Exists(int, lambda d_5_u_:
            (Exists(int, lambda d_6_v_:
                (((((d_2_i_) <= (d_5_u_)) and ((d_5_u_) < (d_6_v_))) and ((d_6_v_) < (len((nums))))) and ((((nums)[d_5_u_]) + ((nums)[d_6_v_])) == (target)),
                        [[(nums)[d_6_v_]]])),
                [[(nums)[d_5_u_]]])))
        d_7_j_ = int(0) # type : int
        d_7_j_ = (d_2_i_) + (1)
        while (d_7_j_) < (len((nums))):
            Invariant(Acc(list_pred(nums)))
            Invariant((2) <= (len((nums))))
            Invariant((((0) <= (d_2_i_)) and ((d_2_i_) < (d_7_j_))) and ((d_7_j_) <= (len((nums)))))
            Invariant(Forall(int, lambda d_8_u_:
                (Forall(int, lambda d_9_v_:
                    (Implies(((((0) <= (d_8_u_)) and ((d_8_u_) < (d_9_v_))) and ((d_9_v_) < (len((nums)))) and (d_8_u_) < (d_2_i_)), (((nums)[d_8_u_]) + ((nums)[d_9_v_])) != (target)),
                           [[(nums)[d_9_v_]]])),
                     [[((nums)[d_8_u_])]])))
            Invariant(Exists(int, lambda d_10_u_:
                (Exists(int, lambda d_11_v_:
                    (((((d_2_i_) <= (d_10_u_)) and ((d_10_u_) < (d_11_v_))) and ((d_11_v_) < (len((nums))))) and ((((nums)[d_10_u_]) + ((nums)[d_11_v_])) == (target)),
                        [[((nums)[d_11_v_])]])),
                    [[((nums)[d_10_u_])]])))
            Invariant(Forall(int, lambda d_12_u_:
                (Implies(((d_2_i_) < (d_12_u_)) and ((d_12_u_) < (d_7_j_)), (((nums)[d_2_i_]) + ((nums)[d_12_u_])) != (target)),
                 [[(nums)[d_12_u_]]])))
            if (((nums)[d_2_i_]) + ((nums)[d_7_j_])) == (target):
                rhs0_ = d_2_i_ # type : int
                rhs1_ = d_7_j_ # type : int
                return (rhs0_, rhs1_)
            d_7_j_ = (d_7_j_) + (1)
        d_2_i_ = (d_2_i_) + (1)
    return (0, 0)