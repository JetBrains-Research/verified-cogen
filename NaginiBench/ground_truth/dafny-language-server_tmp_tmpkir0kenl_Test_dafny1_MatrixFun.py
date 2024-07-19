from typing import List
from nagini_contracts.contracts import *

# def MirrorImage(m : List[List[int]]) -> None:
#     Requires(Acc(list_pred(m)))
#     Requires(Forall(m, lambda m0: Acc(list_pred(m0))))
#     Requires(len(m) > 0)
#     Requires(Forall(int, lambda d_0_i_: Implies(d_0_i_ >= 0 and d_0_i_ < len(m), len(m[0]) == len(m[d_0_i_]))))
#     Ensures(Acc(list_pred(m)))
#     Ensures(Forall(m, lambda m0: Acc(list_pred(m0))))
#     Ensures(len(m) > 0)
#     Ensures(Acc(list_pred(m[0])))
#     Ensures(Acc(list_pred(Old(m))))
#     Ensures(len(m) == Old(len(m)))
#     Ensures(Forall(Old(m), lambda m0:  Acc(list_pred(m0))))
#     Ensures(Forall(int, lambda d_0_i_: Implies(d_0_i_ >= 0 and d_0_i_ < len(m), len(m[0]) == len(m[d_0_i_]) and len(m[0]) == len(Old(m[d_0_i_])))))
#     Ensures(Forall(int, lambda d_0_i_:
#         Forall(int, lambda d_1_j_:
#             Implies((((0) <= (d_0_i_)) and ((d_0_i_) < (len((m))))) and (((0) <= (d_1_j_)) and ((d_1_j_) < (len((m)[0])))), 
#                     ((m)[d_0_i_][d_1_j_]) == (Old(m)[d_0_i_][((len((m)[0])) - (1)) - (d_1_j_)])))))
#     d_2_a_ = int(0) # type : int
#     d_2_a_ = 0
#     while (d_2_a_) < (len((m))):
#         Invariant(Acc(list_pred(m)))
#         Invariant(Forall(m, lambda m0: Acc(list_pred(m0))))
#         Invariant(len(m) > 0)
#         Invariant(len(m) == Old(len(m)))
#         Invariant(Forall(int, lambda d_0_i_: Implies(d_0_i_ >= 0 and d_0_i_ < len(m), len(m[d_0_i_]) == Old(len(m[d_0_i_])))))
#         Invariant(Forall(int, lambda d_0_i_: Implies(d_0_i_ >= 0 and d_0_i_ < len(m), len(m[0]) == len(m[d_0_i_]))))
#         Invariant(0 <= d_2_a_ and (d_2_a_) <= (len((m))))
#         Invariant(Forall(int, lambda d_3_i_:
#             Forall(int, lambda d_4_j_:
#                 Implies(((((0) <= (d_3_i_)) and ((d_3_i_) < (d_2_a_))) and ((0) <= (d_4_j_))) and ((d_4_j_) < (len((m)[0]))), 
#                         ((m)[d_3_i_][d_4_j_]) == (Old((m)[d_3_i_][((len((m)[0])) - (1)) - (d_4_j_)]))))))
#         Invariant(Forall(int, lambda d_5_i_:
#             Forall(int, lambda d_6_j_:
#                 Implies(((((d_2_a_) <= (d_5_i_)) and ((d_5_i_) < (len((m))))) and ((0) <= (d_6_j_))) and ((d_6_j_) < (len((m)[0]))), 
#                         ((m)[d_5_i_][d_6_j_]) == (Old((m)[d_5_i_][d_6_j_]))))))
#         #decreases m.Length0 - a
#         d_7_b_ = int(0) # type : int
#         d_7_b_ = 0
#         while (d_7_b_) < ((len((m)[0]) // 2)):
#             Invariant(Acc(list_pred(m)))
#             Invariant(Forall(m, lambda m0: Acc(list_pred(m0))))
#             Invariant(len(m) > 0)
#             Invariant(len(m) == Old(len(m)))
#             Invariant(Forall(int, lambda d_0_i_: Implies(d_0_i_ >= 0 and d_0_i_ < len(m), len(m[d_0_i_]) == Old(len(m[d_0_i_])))))
#             Invariant(Forall(int, lambda d_0_i_: Implies(d_0_i_ >= 0 and d_0_i_ < len(m), len(m[0]) == len(m[d_0_i_]))))
#             Invariant(0 <= d_2_a_ and (d_2_a_) < (len((m))))
#             Invariant(d_7_b_ >= 0 and (d_7_b_) <= ((len((m)[0]) // 2)))
#             Invariant(Forall(int, lambda d_8_i_:
#                 Forall(int, lambda d_9_j_:
#                     Implies(((((0) <= (d_8_i_)) and ((d_8_i_) < (d_2_a_))) and ((0) <= (d_9_j_))) and ((d_9_j_) < (len((m)[0]))), 
#                             ((m)[d_8_i_][d_9_j_]) == (Old((m)[d_8_i_][((len((m)[0])) - (1)) - (d_9_j_)]))))))
#             Invariant(Forall(int, lambda d_10_j_:
#                 Implies(((0) <= (d_10_j_)) and ((d_10_j_) < (d_7_b_)), 
#                         (((m)[d_2_a_][d_10_j_]) == (Old((m)[d_2_a_][((len((m)[0])) - (1)) - (d_10_j_)]))) and 
#                         ((Old((m)[d_2_a_][d_10_j_])) == ((m)[d_2_a_][((len((m)[0])) - (1)) - (d_10_j_)])))))
#             Invariant(Forall(int, lambda d_11_j_:
#                 Implies(((d_7_b_) <= (d_11_j_)) and ((d_11_j_) < ((len((m)[0])) - (d_7_b_))), 
#                         ((m)[d_2_a_][d_11_j_]) == (Old((m)[d_2_a_][d_11_j_])))))
#             Invariant(Forall(int, lambda d_12_i_:
#                 Forall(int, lambda d_13_j_:
#                     Implies((((((d_2_a_) + (1)) <= (d_12_i_)) and ((d_12_i_) < (len((m))))) and ((0) <= (d_13_j_))) and ((d_13_j_) < (len((m)[0]))), 
#                             ((m)[d_12_i_][d_13_j_]) == (Old((m)[d_12_i_][d_13_j_]))))))
#             #decreases m.Length1 / 2 - b
#             rhs0_ = m[d_2_a_][d_7_b_] # type : int
#             m[d_2_a_][d_7_b_] = m[d_2_a_][((len((m)[0])) - (1)) - (d_7_b_)]
#             m[d_2_a_][((len((m)[0])) - (1)) - (d_7_b_)] = rhs0_
#             d_7_b_ = (d_7_b_) + (1)
#         d_2_a_ = (d_2_a_) + (1)

def Flip(m : List[List[int]]) -> None:
    Requires(Acc(list_pred(m)))
    Requires(Forall(m, lambda m0: Acc(list_pred(m0))))
    Requires(len(m) > 0)
    Requires((len((m))) == (len((m)[0])))
    Requires(Forall(int, lambda d_0_i_: Implies(d_0_i_ >= 0 and d_0_i_ < len(m), len(m[0]) == len(m[d_0_i_]))))
    Ensures(Acc(list_pred(m)))
    Ensures(Forall(m, lambda m0: Acc(list_pred(m0))))
    Ensures(len(m) > 0)
    Ensures(len(m) == Old(len(m)))
    Ensures(Forall(int, lambda i: Implies(i >= 0 and i < len(m), len(m[i]) == Old(len(m[i])))))
    Ensures((len((m))) == (len((m)[0])))
    Ensures(Forall(int, lambda d_0_i_: Implies(d_0_i_ >= 0 and d_0_i_ < len(m), len(m[0]) == len(m[d_0_i_]))))
    Ensures(Forall(int, lambda d_14_i_:
        Forall(int, lambda d_15_j_:
            Implies((((0) <= (d_14_i_)) and ((d_14_i_) < (len((m))))) and (((0) <= (d_15_j_)) and ((d_15_j_) < (len((m)[0])))), 
                    ((m)[d_14_i_][d_15_j_]) == (Old((m)[d_15_j_][d_14_i_]))))))
    d_16_N_ = int(0) # type : int
    d_16_N_ = len((m))
    d_17_a_ = int(0) # type : int
    d_17_a_ = 0
    d_18_b_ = int(0) # type : int
    d_18_b_ = 1
    while (d_17_a_) != (d_16_N_):
        Invariant(Acc(list_pred(m)))
        Invariant(Forall(m, lambda m0: Acc(list_pred(m0))))
        Invariant(len(m) > 0)
        Invariant((len((m))) == (len((m)[0])))
        Invariant(Forall(int, lambda d_0_i_: Implies(d_0_i_ >= 0 and d_0_i_ < len(m), len(m[0]) == len(m[d_0_i_]))))
        Invariant(len(m) == Old(len(m)))
        Invariant(Forall(int, lambda i: Implies(i >= 0 and i < len(m), len(m[i]) == Old(len(m[i])))))
        Invariant(d_17_a_ >= 0)
        Invariant((((d_17_a_) < (d_18_b_)) and ((d_18_b_) <= (d_16_N_)) or 
                   ((d_17_a_) == (d_16_N_)) and ((d_18_b_) == ((d_16_N_) + (1)))))
        Invariant(Forall(int, lambda d_19_i_:
            Forall(int, lambda d_20_j_:
                Implies((((0) <= (d_19_i_)) and ((d_19_i_) <= (d_20_j_))) and ((d_20_j_) < (d_16_N_)), 
                        ((((m)[d_19_i_][d_20_j_]) == (Old((m)[d_20_j_][d_19_i_]))) and (((m)[d_20_j_][d_19_i_]) == (Old((m)[d_19_i_][d_20_j_]))) if (((d_19_i_) < (d_17_a_)) or (((d_19_i_) == (d_17_a_)) and ((d_20_j_) < (d_18_b_)))) else (((m)[d_19_i_][d_20_j_]) == (Old((m)[d_19_i_][d_20_j_]))) and (((m)[d_20_j_][d_19_i_]) == (Old((m)[d_20_j_][d_19_i_]))))))))
        #decreases N - a
        #decreases N - b
        if (d_18_b_) < (d_16_N_):
            rhs0_ = m[d_18_b_][d_17_a_] # type : int
            m[d_18_b_][d_17_a_] = m[d_17_a_][d_18_b_]
            m[d_17_a_][d_18_b_] = rhs0_
            d_18_b_ = (d_18_b_) + (1)
        elif True:
            d_17_a_ = (d_17_a_) + (1)
            d_18_b_ = (d_17_a_) + (1)
