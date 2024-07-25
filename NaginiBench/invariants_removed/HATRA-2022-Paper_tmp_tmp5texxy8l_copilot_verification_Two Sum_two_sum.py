from typing import List, Tuple
from nagini_contracts.contracts import *

def twoSum(nums : List[int], target : int) -> Tuple[int, int]:
    Requires(Acc(list_pred(nums)))
    Requires((2) <= (len((nums))))
    Requires(Exists(int, lambda d_0_i_:
        (Exists(int, lambda d_1_j_:
            (((((0) <= (d_0_i_)) and ((d_0_i_) < (d_1_j_))) and ((d_1_j_) < (len((nums))))) and ((((nums)[d_0_i_]) + ((nums)[d_1_j_])) == (target)),
              [[(nums)[d_1_j_]]])),
        [[(nums)[d_0_i_]]])))
    Ensures(Acc(list_pred(nums)))
    Ensures((Result()[0]) != (Result()[1]))
    Ensures(((0) <= (Result()[0])) and ((Result()[0]) < (len((nums)))))
    Ensures(((0) <= (Result()[1])) and ((Result()[1]) < (len((nums)))))
    Ensures((((nums)[Result()[0]]) + ((nums)[Result()[1]])) == (target))
    d_2_i_ = int(0) # type : int
    while (d_2_i_) < (len((nums))):
        d_7_j_ = int(0) # type : int
        d_7_j_ = (d_2_i_) + (1)
        while (d_7_j_) < (len((nums))):
            if (((nums)[d_2_i_]) + ((nums)[d_7_j_])) == (target):
                rhs0_ = d_2_i_ # type : int
                rhs1_ = d_7_j_ # type : int
                return (rhs0_, rhs1_)
            d_7_j_ = (d_7_j_) + (1)
        d_2_i_ = (d_2_i_) + (1)
    return (0, 0)