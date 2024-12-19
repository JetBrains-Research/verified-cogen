from textwrap import dedent
from verified_cogen.runners.languages import LanguageDatabase, register_basic_languages
from verified_cogen.runners.languages.language import AnnotationType

register_basic_languages(
    with_removed=[
        AnnotationType.INVARIANTS,
        AnnotationType.ASSERTS,
    ]
)


def test_dafny_generate():
    dafny_lang = LanguageDatabase().get("dafny")
    code = dedent(
        """\
        method main(value: int) returns (result: int)
            requires value >= 10
            ensures result >= 20
        {
            assert value * 2 >= 20; // assert-line
            result := value * 2;
        }"""
    )
    assert dafny_lang.generate_validators(code, True) == dedent(
        """\
        method main_valid(value: int) returns (result: int)
            requires value >= 10
            ensures result >= 20
        { var ret0 := main(value); return ret0; }
        """
    )

# def test_dafny_generate1():
#     dafny_lang = LanguageDatabase().get("dafny")
#     code = dedent(
#         """\
# function ParenthesesDepth(s: string, i: int, j: int): int
#     decreases j - i
#     requires 0 <= i <= j <= |s|
# {
#     if i == j then
#         0
#     else if s[i] == '(' then
#         ParenthesesDepth(s, i+1, j) + 1
#     else if s[i] == ')' then
#         ParenthesesDepth(s, i+1, j) - 1
#     else
#         ParenthesesDepth(s, i+1, j)
# }
#
# function InnerDepthsPositive(s: string): bool
# {
#     forall i :: 0 < i < |s| ==> ParenthesesDepth(s, 0, i) > 0
# }
#
# function InnerDepthsNonnegative(s: string): bool
# {
#     forall i :: 0 < i < |s| ==> ParenthesesDepth(s, 0, i) >= 0
# }
#
# lemma ParenthesesDepthSum(s: string, i: int, j: int, k: int)
#     decreases j - i
#     requires 0 <= i <= j <= k <= |s|
#     ensures ParenthesesDepth(s, i, k) == ParenthesesDepth(s, i, j) + ParenthesesDepth(s, j, k)
# {
#     if i != j {
#         ParenthesesDepthSum(s, i+1, j, k);
#     }
# }
#
# lemma ParenthesesSuffixEq(s: string, i: int, j: int)
#     decreases j -i
#     requires 0 <= i <= j <= |s|
#     ensures ParenthesesDepth(s, i, j) == ParenthesesDepth(s[..j], i, j)
# {
#     if i != j {
#         ParenthesesSuffixEq(s, i+1, j);
#     }
# }
#
# lemma ParenthesesPrefixEq(s: string, i: int, j: int)
#     decreases j -i
#     requires 0 <= i <= j <= |s|
#     ensures ParenthesesDepth(s, i, j) == ParenthesesDepth(s[i..], 0, j-i)
# { }
#
# lemma ParenthesesSubstring(s: string, i: int, j: int)
#     decreases j - i
#     requires 0 <= i <= j <= |s|
#     ensures ParenthesesDepth(s, i, j) == ParenthesesDepth(s[i..j], 0, j-i)
# {
#     assert ParenthesesDepth(s, i, j) == ParenthesesDepth(s[..j], i, j)
#         by { ParenthesesSuffixEq(s, i, j); }
#     assert ParenthesesDepth(s[..j], i, j) == ParenthesesDepth(s[i..j], 0, j-i)
#         by { ParenthesesPrefixEq(s[..j], i, j); }
# }
#
# lemma ParenthesesCommonSegment(s: string, t: string, i: int, j: int)
#     requires 0 <= i <= j <= |s|
#     requires 0 <= i <= j <= |t|
#     requires s[i..j] == t[i..j]
#     ensures ParenthesesDepth(s, i, j) == ParenthesesDepth(t, i, j)
# {
#     ParenthesesSubstring(s, i, j);
#     ParenthesesSubstring(t, i, j);
# }
#
# lemma ParenthesesDepthAppend(s: string, c: char)
#     ensures ParenthesesDepth(s + [c], 0, |s|+1) == ParenthesesDepth(s, 0, |s|) + ParenthesesDepth([c], 0, 1)
# {
#     ParenthesesSubstring(s + [c], 0, |s|);
#     ParenthesesSubstring(s + [c], |s|, |s| + 1);
#     ParenthesesDepthSum(s + [c], 0, |s|, |s| + 1);
# }
#
# lemma InnerDepthsPositiveAppendDecompose(s: string, c: char)
#     requires InnerDepthsPositive(s)
#     requires ParenthesesDepth(s, 0, |s|) > 0
#     ensures InnerDepthsPositive(s + [c])
# {
#     forall i: int | 0 < i < |s| + 1
#         ensures ParenthesesDepth(s + [c], 0, i) > 0
#     {
#         if (i <= |s|) {
#             ParenthesesCommonSegment(s, s + [c], 0, i);
#         }
#     }
# }
#
# method separate_paren_groups(paren_string: string) returns (res : seq<string>)
#     // pre-conditions-start
#     requires ParenthesesDepth(paren_string, 0, |paren_string|) == 0
#     requires InnerDepthsNonnegative(paren_string)
#     // pre-conditions-end
#     // post-conditions-start
#     ensures forall k :: 0 <= k < |res| ==> ParenthesesDepth(res[k], 0, |res[k]|) == 0
#     ensures forall k :: 0 <= k < |res| ==> InnerDepthsPositive(res[k])
#     // post-conditions-end
# {
#     // impl-start
#     res := [];
#     var current_string: string := "";
#     var current_depth: int := 0;
#
#     for i := 0 to |paren_string|
#         // invariants-start
#         invariant forall k :: 0 <= k < |res| ==> ParenthesesDepth(res[k], 0, |res[k]|) == 0
#         invariant forall k :: 0 <= k < |res| ==> InnerDepthsPositive(res[k])
#         invariant ParenthesesDepth(paren_string, 0, |paren_string|) == 0
#         invariant InnerDepthsNonnegative(paren_string)
#         invariant ParenthesesDepth(paren_string, i, |paren_string|) + current_depth == 0
#         invariant ParenthesesDepth(paren_string, 0, i) == current_depth
#         invariant ParenthesesDepth(current_string, 0, |current_string|) == current_depth
#         invariant InnerDepthsPositive(current_string)
#         invariant current_string == "" || current_depth > 0
#         invariant current_depth >= 0
#         // invariants-end
#     {
#         var c: char := paren_string[i];
#
#         // lemma-use-start
#         ParenthesesDepthAppend(current_string, c);
#         ParenthesesDepthSum(paren_string, 0, i, i+1);
#         if (current_string != "") {
#             InnerDepthsPositiveAppendDecompose(current_string, c);
#         }
#         // lemma-use-end
#
#         if (c == '(')
#         {
#             current_depth := current_depth + 1;
#             current_string := current_string + [c];
#         }
#         else if (c == ')')
#         {
#             current_depth := current_depth - 1;
#             current_string := current_string + [c];
#
#             if (current_depth == 0)
#             {
#                 res := res + [current_string];
#                 current_string := "";
#             }
#         }
#     }
#     // impl-end
# }
# """
#     )
#     assert dafny_lang.generate_validators(code, True) == dedent(
#         """
#         """
#     )


def test_dafny_generate_with_helper():
    dafny_lang = LanguageDatabase().get("dafny")
    code = dedent(
        """\
        function abs(n: int) : nat { if n > 0 then n else -n }
        
        method main(value: int) returns (result: int)
            requires value >= 10
            ensures result >= 20
        {
            assert value * 2 >= 20; // assert-line
            result := value * 2;
        }"""
    )
    assert dafny_lang.generate_validators(code, True) == dedent(
        """\
        function abs_copy_pure(n: int): nat { 
             if n > 0 then n else -n  
        }
        
        function abs_valid_pure(n: int): nat { abs(n) }
        
        method main_valid(value: int) returns (result: int)
            requires value >= 10
            ensures result >= 20
        { var ret0 := main(value); return ret0; }
        """
    )


def test_dafny_generate_multiple_returns():
    dafny_lang = LanguageDatabase().get("dafny")
    code = dedent(
        """\
        method main(value: int) returns (result: int, result2: int)
            requires value >= 10
            ensures result >= 20
            ensures result2 >= 30
        {
            assert value * 2 >= 20; // assert-line
            result := value * 2;
            result2 := value * 3;
        }"""
    )
    assert dafny_lang.generate_validators(code, True) == dedent(
        """\
        method main_valid(value: int) returns (result: int, result2: int)
            requires value >= 10
            ensures result >= 20
            ensures result2 >= 30
        { var ret0, ret1 := main(value); return ret0, ret1; }
        """
    )


def test_remove_line():
    dafny_lang = LanguageDatabase().get("dafny")
    code = dedent(
        """\
        method main() {
            assert a == 1; // assert-line
        }"""
    )
    assert dafny_lang.remove_conditions(code) == dedent(
        """\
        method main() {
        }"""
    )


def test_remove_multiline_assert():
    dafny_lang = LanguageDatabase().get("dafny")

    code = dedent(
        """\
        method main() {
            // assert-start
            assert a == 1 by {

            }
            // assert-end
        }"""
    )
    assert dafny_lang.remove_conditions(code) == dedent(
        """\
        method main() {
        }"""
    )


def test_remove_invariants():
    dafny_lang = LanguageDatabase().get("dafny")

    code = dedent(
        """\
        method main() {
            while true
                // invariants-start
                invariant false
                invariant true
                // invariants-end
            {
            }
        }"""
    )
    assert dafny_lang.remove_conditions(code) == dedent(
        """\
        method main() {
            while true
            {
            }
        }"""
    )


def test_remove_all():
    dafny_lang = LanguageDatabase().get("dafny")

    code = dedent(
        """\
        method is_prime(k: int) returns (result: bool)
          requires k >= 2
          ensures result ==> forall i :: 2 <= i < k ==> k % i != 0
          ensures !result ==> exists j :: 2 <= j < k && k % j == 0
        {
          var i := 2;
          result := true;
          while i < k
            // invariants-start
            invariant 2 <= i <= k
            invariant !result ==> exists j :: 2 <= j < i && k % j == 0
            invariant result ==> forall j :: 2 <= j < i ==> k % j != 0
            // invariants-end
          {
            if k % i == 0 {
              result := false;
            }
            assert result ==> forall j :: 2 <= j < i ==> k % j != 0; // assert-line
            // assert-start
            assert !result ==> exists j :: 2 <= j < i && k % j == 0 by {
                assert true;
            }
            // assert-end
            i := i + 1;
          }
        }"""
    )
    assert dafny_lang.remove_conditions(code) == dedent(
        """\
        method is_prime(k: int) returns (result: bool)
          requires k >= 2
          ensures result ==> forall i :: 2 <= i < k ==> k % i != 0
          ensures !result ==> exists j :: 2 <= j < k && k % j == 0
        {
          var i := 2;
          result := true;
          while i < k
          {
            if k % i == 0 {
              result := false;
            }
            i := i + 1;
          }
        }"""
    )

