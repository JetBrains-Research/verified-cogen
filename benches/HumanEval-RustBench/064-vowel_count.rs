use vstd::prelude::*;

verus! {

spec fn is_vowel(c: char) -> (ret:bool) {
    c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' || c == 'A' || c == 'E' || c == 'I'
        || c == 'O' || c == 'U'
}
// pure-end

spec fn vowels(s: Seq<char>) -> (ret:Seq<char>) {
    s.filter(|c| is_vowel(c))
}
// pure-end

spec fn inner_expr_vowels_count(s: &str, ret: u32) -> (ret:bool) {
    ret == vowels(s@).len() + if (s@.len() > 0 && (s@.last() == 'y' || s@.last() == 'Y')) {
        1int

    } else {
        0int
    }
}
// pure-end

fn vowels_count(s: &str) -> (ret: u32)
    // pre-conditions-start
    requires
        s@.len() <= u32::MAX,
    // pre-conditions-end
    // post-conditions-start
    ensures
        inner_expr_vowels_count(s, ret),
    // post-conditions-end
{
    // impl-start
    let mut ctr = 0;
    let len = s.unicode_len();
    if len == 0 {
        return ctr;
    }
    assert(len > 0); // assert-line
    let mut i = 0;
    for i in 0..len
        // invariants-start
        invariant
            ctr == vowels(s@.subrange(0, i as int)).len(),
            ctr <= i <= s@.len() == len <= u32::MAX,
            ctr < u32::MAX || is_vowel(s@.last()),
        // invariants-end
    {
        let c = s.get_char(i);
        reveal_with_fuel(Seq::filter, 2);
        assert(s@.subrange(0, i + 1 as int).drop_last() =~= s@.subrange(0, i as int)); // assert-line
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' || c == 'A' || c == 'E' || c
            == 'I' || c == 'O' || c == 'U') {
            ctr += 1;
        }
    }
    // assert-start
    assert(ctr == vowels(s@).len()) by {
        assert(s@.subrange(0, len as int) =~= s@);
    }
    // assert-end
    let c = s.get_char(len - 1);
    if (c == 'y' || c == 'Y') {
        ctr += 1
    }
    ctr
    // impl-end
}

}
fn main() {}
