from typing import List, Optional, Set, Tuple

from nagini_contracts.contracts import *


class Composite:
    def  __init__(self) -> None:
        self.left: Optional[Composite] = None
        self.right: Optional[Composite] = None
        self.parent: Optional[Composite] = None
        self.val: int = int(0)
        self.sum: int = int(0)

    def Valid(self, S : Set[Composite]) -> bool :
        Requires(Acc(set_pred(S)))
        Requires(Acc(self.left))
        Requires(Acc(self.right))
        Requires(Acc(self.parent))
        Requires(Acc(self.val))
        Requires(Acc(self.sum))
        Requires(Implies(self.parent is not None, Acc(self.parent.left)))
        Requires(Implies(self.parent is not None, Acc(self.parent.right)))
        Requires(Implies(self.left is not None, Acc(self.left.parent)))
        Requires(Implies(self.left is not None, Acc(self.left.sum)))
        Requires(Implies(self.right is not None, Acc(self.right.parent)))
        Requires(Implies(self.right is not None, Acc(self.right.sum)))
        return ((((((self) in (S)) and (not ((self.parent) != (None)) or (((self.parent) in (S)) and (((self.parent.left) == (self)) or ((self.parent.right) == (self)))))) and 
                 (not ((self.left) != (None)) or ((((self.left) in (S)) and ((self.left.parent) == (self))) and ((self.left) != (self.right))))) and 
                 (not ((self.right) != (None)) or ((((self.right) in (S)) and ((self.right.parent) == (self))) and ((self.left) != (self.right))))) and 
                ((self.sum) == (((self.val) + ((0 if (self.left) == (None) else self.left.sum))) + ((0 if (self.right) == (None) else self.right.sum)))))

    

    def Acyclic(self, S : Set[Composite]) -> bool :
        Requires(Acc(set_pred(S)))
        Requires(Acc(self.parent))
        S1 = set({self}) # type : Set[Composite]
        S2 = S # type : Set[Composite]
        return ((self) in (S)) and (Implies((self.parent) != (None), ((self.parent) is not (None)) and (self.parent).Acyclic(S2)))

    # def Init(self, x : int) -> None:
    #     Ensures(((((self).Valid(set({self}))) and ((self).Acyclic(set({self})))) and ((self.val) == (x))) and ((self.parent) == (None)))
    #     (self).parent = None
    #     (self).left = None
    #     (self).right = None
    #     (self).val = x
    #     (self).sum = self.val

    # def Update(self, x : int, S : Set[Composite]) -> None:
    #     Requires(Acc(set_pred(S)))
    #     Requires(((self) in (S)) and ((self).Acyclic(S)))
    #     Requires(Forall(Composite, lambda d_7_c_:
    #         not ((d_7_c_) in (S)) or ((d_7_c_).Valid(S))))
    #     Ensures(Acc(set_pred(S)))
    #     Ensures(Forall(Composite, lambda d_8_c_:
    #         not ((d_8_c_) in (S)) or ((d_8_c_).Valid(S))))
    #     Ensures(Forall(Composite, lambda d_9_c_:
    #         not ((d_9_c_) in (S)) or ((((d_9_c_.left) == (Old(d_9_c_.left))) and ((d_9_c_.right) == (Old(d_9_c_.right)))) and ((d_9_c_.parent) == (Old(d_9_c_.parent))))))
    #     Ensures(Forall(Composite, lambda d_10_c_:
    #         not (((d_10_c_) in (S)) and ((d_10_c_) != (self))) or ((d_10_c_.val) == (Old(d_10_c_.val)))))
    #     Ensures((self.val) == (x))
    #     d_11_delta_ = int(0) # type : int
    #     d_11_delta_ = (x) - (self.val)
    #     (self).val = x
    #     (self).Adjust(d_11_delta_, S, S)

    # def Add(self, S : Set[Composite], child : Composite, U : Set[Composite]) -> None:
    #     Requires(Acc(set_pred(U)))
    #     Requires(Acc(set_pred(S)))
    #     Requires(((self) in (S)) and ((self).Acyclic(S)))
    #     Requires(Forall(Composite, lambda d_12_c_:
    #         not ((d_12_c_) in (S)) or ((d_12_c_).Valid(S))))
    #     Requires((child) in (U))
    #     Requires(Forall(Composite, lambda d_13_c_:
    #         not ((d_13_c_) in (U)) or ((d_13_c_).Valid(U))))
    #     Requires((S).isdisjoint(U))
    #     Requires(((self.left) == (None)) or ((self.right) == (None)))
    #     Requires((child.parent) == (None))
    #     Ensures(Acc(set_pred(U)))
    #     Ensures(Acc(set_pred(S)))
    #     Ensures((((child.left) == (Old(child.left))) and ((child.right) == (Old(child.right)))) and ((child.val) == (Old(child.val))))
    #     Ensures(Forall(Composite, lambda d_14_c_:
    #         not (((d_14_c_) in (S)) and ((d_14_c_) != (self))) or (((d_14_c_.left) == (Old(d_14_c_.left))) and ((d_14_c_.right) == (Old(d_14_c_.right))))))
    #     Ensures(not ((Old(self.left)) != (None)) or ((self.left) == (Old(self.left))))
    #     Ensures(not ((Old(self.right)) != (None)) or ((self.right) == (Old(self.right))))
    #     Ensures(Forall(Composite, lambda d_15_c_:
    #         not ((d_15_c_) in (S)) or (((d_15_c_.parent) == (Old(d_15_c_.parent))) and ((d_15_c_.val) == (Old(d_15_c_.val))))))
    #     Ensures((child.parent) == (self))
    #     Ensures(Forall(Composite, lambda d_16_c_:
    #         not ((d_16_c_) in ((S) | (U))) or ((d_16_c_).Valid((S) | (U)))))
    #     if (self.left) == (None):
    #         (self).left = child
    #     elif True:
    #         (self).right = child
    #     (child).parent = self
    #     (self).Adjust(child.sum, S, S | U)

    # def Dislodge(self, S : Set[Composite]) -> None:
    #     Requires(Acc(set_pred(S)))
    #     Requires(((self) in (S)) and ((self).Acyclic(S)))
    #     Requires(Forall(Composite, lambda d_17_c_:
    #         not ((d_17_c_) in (S)) or ((d_17_c_).Valid(S))))
    #     Ensures(Acc(set_pred(S)))
    #     Ensures(Forall(Composite, lambda d_18_c_:
    #         not ((d_18_c_) in (S)) or ((d_18_c_).Valid(S))))
    #     Ensures(Forall(Composite, lambda d_19_c_:
    #         not ((d_19_c_) in (S)) or ((d_19_c_.val) == (Old(d_19_c_.val)))))
    #     Ensures(Forall(Composite, lambda d_20_c_:
    #         not (((d_20_c_) in (S)) and ((d_20_c_) != (self))) or ((d_20_c_.parent) == (Old(d_20_c_.parent)))))
    #     Ensures((self.parent) == (None))
    #     Ensures(Forall(Composite, lambda d_21_c_:
    #         not ((d_21_c_) in (S)) or (((d_21_c_.left) == (Old(d_21_c_.left))) or (((Old(d_21_c_.left)) == (self)) and ((d_21_c_.left) == (None))))))
    #     Ensures(Forall(Composite, lambda d_22_c_:
    #         not ((d_22_c_) in (S)) or (((d_22_c_.right) == (Old(d_22_c_.right))) or (((Old(d_22_c_.right)) == (self)) and ((d_22_c_.right) == (None))))))
    #     Ensures((self).Acyclic(set({self})))
    #     d_23_p_ = None # type : Composite
    #     d_23_p_ = self.parent
    #     (self).parent = None
    #     if (d_23_p_) is not (None):
    #         if (d_23_p_.left) == (self):
    #             (d_23_p_).left = None
    #         elif True:
    #             (d_23_p_).right = None
    #         d_24_delta_ = int(0) # type : int
    #         d_24_delta_ = (0) - (self.sum)
    #         (d_23_p_).Adjust(d_24_delta_, S - {self}, S)

    # def Adjust(self, delta : int, U : Set[Composite], S : Set[Composite]) -> None:
    #     Requires(Acc(set_pred(S)))
    #     Requires(Acc(set_pred(U)))
    #     Requires(((U).issubset(S)) and ((self).Acyclic(U)))
    #     Requires(Forall(Composite, lambda d_25_c_:
    #         not (((d_25_c_) in (S)) and ((d_25_c_) != (self))) or ((d_25_c_).Valid(S))))
    #     Requires(not ((self.parent) != (None)) or (((self.parent) in (S)) and (((self.parent.left) == (self)) or ((self.parent.right) == (self)))))
    #     Requires(not ((self.left) != (None)) or ((((self.left) in (S)) and ((self.left.parent) == (self))) and ((self.left) != (self.right))))
    #     Requires(not ((self.right) != (None)) or ((((self.right) in (S)) and ((self.right.parent) == (self))) and ((self.left) != (self.right))))
    #     Requires(((self.sum) + (delta)) == (((self.val) + ((0 if (self.left) is (None) else self.left.sum))) + ((0 if (self.right) is (None) else self.right.sum))))
    #     Ensures(Acc(set_pred(S)))
    #     Ensures(Acc(set_pred(U)))
    #     Ensures(Forall(Composite, lambda d_26_c_:
    #         not ((d_26_c_) in (S)) or ((d_26_c_).Valid(S))))
    #     d_27_p_ = None # type : Optional[Composite]
    #     d_27_p_ = self
    #     d_28_T_ = U # type : Set[Composite]
    #     while (d_27_p_) is not (None):
    #         Invariant(Acc(set_pred(S)))
    #         Invariant(Acc(set_pred(U)))
    #         Invariant((d_28_T_).issubset(U))
    #         Invariant(((d_27_p_) == (None)) or ((d_27_p_).Acyclic(d_28_T_)))
    #         Invariant(Forall(Composite, lambda d_29_c_:
    #             not (((d_29_c_) in (S)) and ((d_29_c_) != (d_27_p_))) or ((d_29_c_).Valid(S))))
    #         Invariant(not ((d_27_p_) != (None)) or (((d_27_p_.sum) + (delta)) == (((d_27_p_.val) + ((0 if (d_27_p_.left) == (None) else d_27_p_.left.sum))) + ((0 if (d_27_p_.right) == (None) else d_27_p_.right.sum)))))
    #         Invariant(Forall(Composite, lambda d_30_c_:
    #             not ((d_30_c_) in (S)) or (((((d_30_c_.left) == (Old(d_30_c_.left))) and ((d_30_c_.right) == (Old(d_30_c_.right)))) and ((d_30_c_.parent) == (Old(d_30_c_.parent)))) and ((d_30_c_.val) == (Old(d_30_c_.val))))))
    #         #decreases T
    #         (d_27_p_).sum = (d_27_p_.sum) + (delta)
    #         d_28_T_ = d_28_T_ - {d_27_p_}
    #         d_27_p_ = d_27_p_.parent