from textwrap import dedent
from verified_cogen.runners.languages import LanguageDatabase, register_basic_languages
from verified_cogen.runners.languages.language import AnnotationType

register_basic_languages(
    with_removed=[
        AnnotationType.INVARIANTS,
        AnnotationType.ASSERTS,
        AnnotationType.PRE_CONDITIONS,
        AnnotationType.POST_CONDITIONS,
        AnnotationType.IMPLS,
        AnnotationType.PURE,
    ]
)


def test_nagini_large():
    nagini_lang = LanguageDatabase().get("nagini")

    code = dedent(
        """\
        from typing import cast, List, Dict, Set, Optional, Union
        from nagini_contracts.contracts import *

        @Pure
        def lower(c : int) -> bool :
            # pure-start
            return ((0) <= (c)) and ((c) <= (25))
            # pure-end

        @Pure
        def upper(c : int) -> bool :
            # pure-start
            return ((26) <= (c)) and ((c) <= (51))
            # pure-end

        @Pure
        def alpha(c : int) -> bool :
            # pure-start
            return (lower(c)) or (upper(c))
            # pure-end

        @Pure
        def flip__char(c : int) -> int :
            # post-conditions-start
            Ensures(lower(c) == upper(Result()))
            Ensures(upper(c) == lower(Result()))
            # post-conditions-end

            # pure-start
            if lower(c):
                return ((c) - (0)) + (26)
            elif upper(c):
                return ((c) + (0)) - (26)
            elif True:
                return c
            # pure-end

        def flip__case(s : List[int]) -> List[int] :
            # pre-conditions-start
            Requires(Acc(list_pred(s)))
            # pre-conditions-end
            # post-conditions-start
            Ensures(Acc(list_pred(s)))
            Ensures(Acc(list_pred(Result())))
            Ensures((len(Result())) == (len(s)))
            Ensures(Forall(int, lambda d_0_i_: (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(s))), lower((s)[d_0_i_]) == upper((Result())[d_0_i_])))))
            Ensures(Forall(int, lambda d_0_i_: (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(s))), upper((s)[d_0_i_]) == lower((Result())[d_0_i_])))))
            # post-conditions-end

            # impl-start
            res = list([int(0)] * len(s)) # type : List[int]
            i = int(0) # type : int
            while i < len(s):
                # invariants-start
                Invariant(Acc(list_pred(s)))
                Invariant(Acc(list_pred(res)))
                Invariant(((0) <= (i)) and ((i) <= (len(s))))
                Invariant((len(res)) == (len(s)))
                Invariant(Forall(int, lambda d_0_i_: (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (i)), lower((s)[d_0_i_]) == upper((res)[d_0_i_])))))
                Invariant(Forall(int, lambda d_0_i_: (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (i)), upper((s)[d_0_i_]) == lower((res)[d_0_i_])))))
                # invariants-end
                res[i] = flip__char(s[i])
                i = i + 1
            return res
            # impl-end"""
    )
    assert nagini_lang.generate_validators(code, False) == dedent(
        """\

        @Pure
        def lower_copy_pure(c : int) -> bool :

            return ((0) <= (c)) and ((c) <= (25))

        @Pure
        def upper_copy_pure(c : int) -> bool :

            return ((26) <= (c)) and ((c) <= (51))

        @Pure
        def alpha_copy_pure(c : int) -> bool :

            return (lower_copy_pure(c)) or (upper_copy_pure(c))

        @Pure
        def flip__char_copy_pure(c : int) -> int :
            # post-conditions-start
            Ensures(lower_copy_pure(c) == upper_copy_pure(Result()))
            Ensures(upper_copy_pure(c) == lower_copy_pure(Result()))
            # post-conditions-end
            if lower_copy_pure(c):
                return ((c) - (0)) + (26)
            elif upper_copy_pure(c):
                return ((c) + (0)) - (26)
            elif True:
                return c
            
        def flip__case_valid(s : List[int]) -> List[int] :
            # pre-conditions-start
            Requires(Acc(list_pred(s)))
            # pre-conditions-end
            # post-conditions-start
            Ensures(Acc(list_pred(s)))
            Ensures(Acc(list_pred(Result())))
            Ensures((len(Result())) == (len(s)))
            Ensures(Forall(int, lambda d_0_i_: (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(s))), lower_copy_pure((s)[d_0_i_]) == upper_copy_pure((Result())[d_0_i_])))))
            Ensures(Forall(int, lambda d_0_i_: (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(s))), upper_copy_pure((s)[d_0_i_]) == lower_copy_pure((Result())[d_0_i_])))))
            # post-conditions-end

            ret = flip__case(s)
            return ret"""
    )


def test_nagini_large1():
    nagini_lang = LanguageDatabase().get("nagini")

    code = dedent(
        """\
        from typing import cast, List, Dict, Set, Optional, Union
        from nagini_contracts.contracts import *
        
        def fizz__buzz(n : int) -> int:
            # pre-conditions-start
            Requires(n >= 0)
            # pre-conditions-end
            # post-conditions-start
            Ensures(Result() >= 0)
            Ensures((Result()) == fizz_buzz_fun(n))
            # post-conditions-end
        
            # impl-start
            result : int = 0
            i : int = 0
            while (i) < (n):
                # invariants-start
                Invariant(((0) <= (i)) and ((i) <= (n)))
                Invariant(Forall(int, lambda x : (Implies(x >= 0 and x < n, 
                    fizz_buzz_fun(x + 1) == (count7__r(x) if ((x % 11 == 0) or (x % 13 == 0)) else 0) + fizz_buzz_fun(x)), [[fizz_buzz_fun(x + 1)]])))
                Invariant(result == fizz_buzz_fun(i))
                # invariants-end
                if (((i % 11)) == (0)) or (((i % 13)) == (0)):
                    cnt : int = count7(i)
                    result = (result) + (cnt)
                i = (i) + (1)
            return result
            # impl-end
        
        @Pure
        
        def fizz_buzz_fun(n : int) -> int:
            # pure-pre-conditions-start
            Requires(n >= 0)
            # pure-pre-conditions-end
            # pure-post-conditions-start
            Ensures(Result() >= 0)
            # pure-post-conditions-end
        
            # pure-start
            if n == 0:
                return 0
            else:
                return (count7__r(n - 1) if ((n - 1) % 11 == 0 or (n - 1) % 13 == 0) else 0) + fizz_buzz_fun(n - 1)
            # pure-end
        
        
        def count7(x : int) -> int:
            # pre-conditions-start
            Requires(x >= 0)
            # pre-conditions-end
            # post-conditions-start
            Ensures(Result() >= 0)
            Ensures((Result()) == (count7__r(x)))
            # post-conditions-end
        
            # impl-start
            count : int = 0
            y : int = x
            while (y) > (0):
                # invariants-start
                Invariant(((0) <= (y)) and ((y) <= (x)))
                Invariant(((count) + (count7__r(y))) == (count7__r(x)))
                # invariants-end
                if ((y % 10)) == (7):
                    count = (count) + (1)
                y = y // 10
            return count
            # impl-end  
        
        @Pure
        def count7__r(x : int) -> int :
            # pure-pre-conditions-start
            Requires(x >= 0)
            # pure-pre-conditions-end
            # pure-post-conditions-start
            Ensures(Result() >= 0)
            # pure-post-conditions-end
        
            # pure-start
            if x == 0:
                return 0
            else:
                return (x % 10 == 7) + count7__r(x // 10)
            # pure-end"""
    )

    assert nagini_lang.remove_conditions(code) == dedent(
        """\
        from typing import cast, List, Dict, Set, Optional, Union
        from nagini_contracts.contracts import *
        def fizz__buzz(n : int) -> int:
        def count7(x : int) -> int:"""
    )


def test_nagini_large2():
    nagini_lang = LanguageDatabase().get("nagini")

    code = dedent(
        """\
        from typing import cast, List, Dict, Set, Optional, Union
        from nagini_contracts.contracts import *
        
        def parseparengroup(s : List[int]) -> int:
            # pre-conditions-start
            Requires(Acc(list_pred(s), 1/2))
            Requires(contains12(s))
            Requires(get_len(s))
            # pre-conditions-end
            # post-conditions-start
            Ensures(Acc(list_pred(s), 1/2))
            Ensures(contains12(s))
            Ensures(get_len(s))
            Ensures((Result()) >= (0))
            # post-conditions-end
        
            # impl-start
            depth : int = 0
            max__depth : int = 0
            i : int = 0
            while (i) < (len(s)):
                # invariants-start
                Invariant(Acc(list_pred(s), 1/2))
                Invariant(((i) >= (0)) and ((i) <= (len(s))))
                Invariant(max__depth >= 0)
                Invariant(contains12(s))
                Invariant(get_len(s))
                # invariants-end
                c : int = (s)[i]
                if (c) == (1):
                    depth = (depth) + (1)
                    if (depth) > (max__depth):
                        max__depth = depth
                else:
                    depth = (depth) - (1)
                i = (i) + (1)
            return max__depth
            # impl-end
        
        @Pure 
        def get_len(s : List[int]) -> bool:
            # pure-pre-conditions-start
            Requires(Acc(list_pred(s), 1/2))
            # pure-pre-conditions-end
        
            # pure-start
            return len(s) > 0
            # pure-end
        
        @Pure 
        def contains12(s : List[int]) -> bool:
            # pure-pre-conditions-start
            Requires(Acc(list_pred(s), 1/2))
            # pure-pre-conditions-end
        
            # pure-start
            return Forall(int, lambda i: 
                Implies(i >= 0 and i < len(s), s[i] == 1 or s[i] == 2))
            # pure-end
        
        def split(s : List[int]) -> List[List[int]]:
            # pre-conditions-start
            Requires(Acc(list_pred(s)))
            Requires(Forall(int, lambda i:
                not (((i) >= (0)) and ((i) < (len(s)))) or (((((s)[i]) == (1)) or (((s)[i]) == (2))) or (((s)[i]) == (3)))))
            # pre-conditions-end
            # post-conditions-start
            Ensures(Acc(list_pred(ResultT(List[List[int]]))))
            Ensures(Forall(ResultT(List[List[int]]), lambda x: Acc(list_pred(x), 1/2)))
            Ensures(Forall(int, lambda j:
                Implies(j >= 0 and j < len(ResultT(List[List[int]])), (get_len(ResultT(List[List[int]])[j])))))
            Ensures(Forall(int, lambda j:
                (Implies(j >= 0 and j < len(Result()), 
                    contains12(Result()[j])), [[contains12(Result()[j])]])))
            # post-conditions-end
        
            # impl-start
            res : List[List[int]] = []
            current__string : List[int] = []
            i : int = 0
            while (i) < (len(s)):
                # invariants-start
                Invariant(Acc(list_pred(res)))
                Invariant(Forall(res, lambda x: Acc(list_pred(x), 1/2)))
                Invariant(Acc(list_pred(current__string)))
                Invariant(Acc(list_pred(s)))
                Invariant(((i) >= (0)) and ((i) <= (len(s))))
                Invariant(Forall(int, lambda i:
                    (not (((i) >= (0)) and ((i) < (len(s)))) or (((((s)[i]) == (1)) or 
                     (((s)[i]) == (2))) or (((s)[i]) == (3))), [[]])))
                Invariant(Forall(int, lambda i:
                    (not (((i) >= (0)) and ((i) < (len(current__string)))) or 
                     (((((current__string)[i]) == (1)) or (((current__string)[i]) == (2)))), [[]])))
                Invariant(Forall(int, lambda j:
                    (Implies(j >= 0 and j < len(res), ((get_len(res[j])))), [[]])))
                Invariant(Forall(int, lambda j:
                    (Implies(j >= 0 and j < len(res), 
                        contains12(res[j])), [[contains12(res[j])]])))
                # invariants-end
                if ((s)[i]) == (3):
                    if len(current__string) > 0:
                        d_7_copy = list(current__string)
                        res = (res) + [d_7_copy]
                        current__string = []
                else:
                    current__string = (current__string) + [(s)[i]]
                i = (i) + (1)
            if len(current__string) > 0:
                d_7_copy = list(current__string)
                # assert-start
                Assert(get_len(d_7_copy))
                # assert-end
                res = (res) + [d_7_copy]
                current__string =  []
            return res
            # impl-end
        
        def parse__nested__parens(paren__string : List[int]) -> List[int]:
            # pre-conditions-start
            Requires(Acc(list_pred(paren__string)))
            Requires(Forall(int, lambda i:
                not (((i) >= (0)) and ((i) < (len(paren__string)))) or (((((paren__string)[i]) == (3)) or (((paren__string)[i]) == (1))) or (((paren__string)[i]) == (2)))))
            # pre-conditions-end
            # post-conditions-start
            Ensures(Acc(list_pred(Result())))
            Ensures(Forall(ResultT(List[int]), lambda x: ((x) >= (0))))
            # post-conditions-end
        
            # impl-start
            res : List[int] = []
            strings : List[List[int]] = split(paren__string)
            i : int = int(0)
            while (i) < (len(strings)):
                # invariants-start
                Invariant(Acc(list_pred(strings)))
                Invariant(Acc(list_pred(res)))
                Invariant(Forall(strings, lambda x: Acc(list_pred(x), 1/2)))
                Invariant(0 <= i and i <= len(strings))
                Invariant(Forall(res, lambda x: ((x) >= (0))))
                Invariant(Forall(int, lambda j:
                    Implies(j >= 0 and j < len(strings), (get_len(strings[j])))))
                Invariant(Forall(int, lambda j:
                    (Implies(j >= 0 and j < len(strings), 
                        contains12(strings[j])), [[contains12(strings[j])]])))
                # invariants-end
                cur : int = parseparengroup((strings)[i])
                res = (res) + [cur]
                i = (i) + (1)
            return res
            # impl-end"""
    )

    assert nagini_lang.remove_conditions(code) == dedent(
        """\
        from typing import cast, List, Dict, Set, Optional, Union
        from nagini_contracts.contracts import *
        def parseparengroup(s : List[int]) -> int:
        def split(s : List[int]) -> List[List[int]]:
        def parse__nested__parens(paren__string : List[int]) -> List[int]:"""
    )