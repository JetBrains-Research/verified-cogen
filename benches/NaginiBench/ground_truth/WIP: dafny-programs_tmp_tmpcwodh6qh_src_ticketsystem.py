from typing import Dict, List, Literal, NamedTuple, NewType, Set, Tuple

from nagini_contracts.contracts import *

CState = Literal['Thinking', 'Hungry', 'Eating']
# CState = NewType('CState', CState)

# int = NewType('int', int)

class TicketSystem:

    def __init__(self, processes : Set[int]) -> None:
        Requires(Acc(set_pred(processes)))
        Ensures(Acc(set_pred(processes)))
        Ensures((self).Valid())
        self.P = processes
        rhs0_ = 0 # type : int
        rhs1_ = 0 # type : int
        self.ticket = rhs0_
        self.serving = rhs1_
        def iife0_() -> Dict[int, CState]:
            coll0_ : Dict[int, CState] = dict() # type : Dict[int, CState]
            compr_0_ = int(0) # type : int
            for compr_0_ in (processes):
                d_4_p_: int = compr_0_
                if (d_4_p_) in (processes):
                    coll0_[d_4_p_] = ('Thinking')
            return dict(coll0_)
        (self).cs = iife0_()
        
        def iife1_() -> Dict[int, int]:
            coll1_ = dict() # type : Dict[int, int]
            compr_1_ = int(0) # type : int
            for compr_1_ in (processes):
                d_5_p_: int = compr_1_
                if (d_5_p_) in (processes):
                    coll1_[d_5_p_] = 0
            return dict(coll1_)
        (self).t = iife1_()
        
    def Valid(self) -> bool :
        return (((((((self).P).issubset((self.cs).keys())) and (((self).P).issubset((self.t).keys()))) and ((self.serving) <= (self.ticket))) and (Forall(int, lambda d_0_p_:
            not (((d_0_p_) in ((self).P)) and (((self.cs)[d_0_p_]) != (('Thinking')))) or (((self.serving) <= ((self.t)[d_0_p_])) and (((self.t)[d_0_p_]) < (self.ticket)))))) and (Forall(int, lambda d_1_p_:
            Forall(int, lambda d_2_q_:
                not ((((((d_1_p_) in ((self).P)) and ((d_2_q_) in ((self).P))) and ((d_1_p_) != (d_2_q_))) and (((self.cs)[d_1_p_]) != (('Thinking')))) and (((self.cs)[d_2_q_]) != (('Thinking')))) or (((self.t)[d_1_p_]) != ((self.t)[d_2_q_])))))) and (Forall(int, lambda d_3_p_:
            not (((d_3_p_) in ((self).P)) and (((self.cs)[d_3_p_]) == (('Eating')))) or (((self.t)[d_3_p_]) == (self.serving))))

    def Request(self, p : int) -> None:
        Requires((((self).Valid()) and ((p) in ((self).P))) and (((self.cs)[p]) == (('Thinking'))))
        Ensures((self).Valid())
        (self.t)[p] = (self.ticket)
        self.ticket = (self.ticket) + (1) 
        (self).cs[p] = ('Hungry')

    def Enter(self, p : int) -> None:
        Requires((((self).Valid()) and ((p) in ((self).P))) and (((self.cs)[p]) == ('Hungry')))
        Ensures((self).Valid())
        if ((self.t)[p]) == (self.serving):
            (self).cs[p] = ('Eating')

    def Leave(self, p : int) -> None:
        Requires((((self).Valid()) and ((p) in ((self).P))) and (((self.cs)[p]) == (('Eating'))))
        Ensures((self).Valid())
        Assert(((self.t)[p]) == (self.serving))
        (self).serving = (self.serving) + (1)
        (self).cs[p] = 'Thinking'
