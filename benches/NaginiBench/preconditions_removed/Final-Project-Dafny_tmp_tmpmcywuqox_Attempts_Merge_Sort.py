from typing import List, Tuple

from nagini_contracts.contracts import *


def merging(a : List[int], low : int, medium : int, high : int) -> None:
    Ensures(Acc(list_pred(a)))
    Ensures(len(a) == Old(len(a)))
    d_0_x_ = int(0) # type : int
    d_0_x_ = 0
    d_1_y_ = int(0) # type : int
    d_1_y_ = 0
    d_2_z_ = int(0) # type : int
    d_2_z_ = 0
    d_3_a1_ = [int(0)] * 0 # type : List[int]
    nw0_ = [int(0)] * (((medium) - (low)) + (1)) # type : List[int]
    d_3_a1_ = nw0_
    d_4_a2_ = [int(0)] * 0 # type : List[int]
    nw1_ = [int(0)] * ((high) - (medium)) # type : List[int]
    d_4_a2_ = nw1_
    while ((d_1_y_) < (len((d_3_a1_)))) and (((low) + (d_1_y_)) < (len((a)))):
        Invariant(Acc(list_pred(d_4_a2_)))
        Invariant(Acc(list_pred(d_3_a1_)))
        Invariant(Acc(list_pred(a)))
        Invariant(len(a) == Old(len(a)))
        Invariant(((((0) <= (low)) and ((low) <= (medium))) and ((medium) <= (high))) and ((high) < (len((a)))))
        Invariant(((0) <= (d_1_y_)) and ((d_1_y_) <= (len((d_3_a1_)))))
        Invariant(((0) <= ((low) + (d_1_y_))) and (((low) + (d_1_y_)) <= (len((a)))))
        (d_3_a1_)[(d_1_y_)] = (a)[(low) + (d_1_y_)]
        d_1_y_ = (d_1_y_) + (1)
    while ((d_2_z_) < (len((d_4_a2_)))) and ((((medium) + (d_2_z_)) + (1)) < (len((a)))):
        Invariant(Acc(list_pred(d_4_a2_)))
        Invariant(Acc(list_pred(d_3_a1_)))
        Invariant(Acc(list_pred(a)))
        Invariant(len(a) == Old(len(a)))
        Invariant(((((0) <= (low)) and ((low) <= (medium))) and ((medium) <= (high))) and ((high) < (len((a)))))
        Invariant(((0) <= (d_1_y_)) and ((d_1_y_) <= (len((d_3_a1_)))))
        Invariant(((0) <= (d_2_z_)) and ((d_2_z_) <= (len((d_4_a2_)))))
        Invariant(((0) <= ((medium) + (d_2_z_))) and (((medium) + (d_2_z_)) <= (len((a)))))
        (d_4_a2_)[(d_2_z_)] = (a)[((medium) + (d_2_z_)) + (1)]
        d_2_z_ = (d_2_z_) + (1)
    rhs0_ = 0 # type : int
    rhs1_ = 0 # type : int
    d_1_y_ = rhs0_
    d_2_z_ = rhs1_
    while ((((d_0_x_) < (((high) - (low)) + (1))) and ((d_1_y_) <= (len((d_3_a1_))))) and ((d_2_z_) <= (len((d_4_a2_))))) and (((low) + (d_0_x_)) < (len((a)))):
        Invariant(Acc(list_pred(d_4_a2_)))
        Invariant(Acc(list_pred(d_3_a1_)))
        Invariant(Acc(list_pred(a)))
        Invariant(len(a) == Old(len(a)))
        Invariant(((0) <= (d_1_y_)) and ((d_1_y_) <= (len((d_3_a1_)))))
        Invariant(((0) <= (d_2_z_)) and ((d_2_z_) <= (len((d_4_a2_)))))
        Invariant(((0) <= (d_0_x_)) and ((d_0_x_) <= (((high) - (low)) + (1))))
        if ((d_1_y_) >= (len((d_3_a1_)))) and ((d_2_z_) >= (len((d_4_a2_)))):
            break
        elif (d_1_y_) >= (len((d_3_a1_))):
            index0_ = (low) + (d_0_x_) # type : int
            (a)[index0_] = (d_4_a2_)[d_2_z_]
            d_2_z_ = (d_2_z_) + (1)
        elif (d_2_z_) >= (len((d_4_a2_))):
            index1_ = (low) + (d_0_x_) # type : int
            (a)[index1_] = (d_3_a1_)[d_1_y_]
            d_1_y_ = (d_1_y_) + (1)
        elif True:
            if ((d_3_a1_)[d_1_y_]) <= ((d_4_a2_)[d_2_z_]):
                index2_ = (low) + (d_0_x_) # type : int
                (a)[index2_] = (d_3_a1_)[d_1_y_]
                d_1_y_ = (d_1_y_) + (1)
            elif True:
                index3_ = (low) + (d_0_x_) # type : int
                (a)[index3_] = (d_4_a2_)[d_2_z_]
                d_2_z_ = (d_2_z_) + (1)
        d_0_x_ = (d_0_x_) + (1)

def sorting(a : List[int], low : int, high : int) -> None:
    Ensures(Acc(list_pred(a)))
    Ensures(len(a) == Old(len(a)))
    if (low) < (high):
        d_5_medium_ = int(0) # type : int
        d_5_medium_ = (low) + (((high) - (low)) // 2)
        sorting(a, low, d_5_medium_)
        sorting(a, (d_5_medium_) + (1), high)
        merging(a, low, d_5_medium_, high)