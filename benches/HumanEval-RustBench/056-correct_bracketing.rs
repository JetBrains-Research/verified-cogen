use vstd::prelude::*;

verus! {

spec fn spec_bracketing_helper(brackets: Seq<char>) -> (result:(int, bool)) {
    brackets.fold_left(
        (0, true),
        |p: (int, bool), c|
            {
                let (x, b) = p;
                match (c) {
                    '<' => (x + 1, b),
                    '>' => (x - 1, b && x - 1 >= 0),
                    _ => (x, b),
                }
            },
    )
}
// pure-end

spec fn spec_bracketing(brackets: Seq<char>) -> (result:bool) {
    let p = spec_bracketing_helper(brackets);
    p.1 && p.0 == 0
}
// pure-end

fn correct_bracketing(brackets: &str) -> (ret: bool)
    // pre-conditions-start
    requires
        brackets@.len() <= i32::MAX,
        -brackets@.len() >= i32::MIN,
    // pre-conditions-end
    // post-conditions-start
    ensures
        ret <==> spec_bracketing(brackets@),
    // post-conditions-end
{
    // impl-start
    let mut i = 0;
    let mut b = true;
    let mut stack_size: i32 = 0;

    while i < brackets.unicode_len()
        // invariants-start
        invariant
            (stack_size as int, b) == spec_bracketing_helper(brackets@.subrange(0, i as int)),
            stack_size <= i <= brackets@.len() <= i32::MAX,
            stack_size >= -i >= -brackets@.len() >= i32::MIN,
        // invariants-end
    {
        let c = brackets.get_char(i);
        if (c == '<') {
            stack_size += 1;
        } else if (c == '>') {
            b = b && stack_size > 0;
            stack_size -= 1;
        }
        // assert-start
        assert(brackets@.subrange(0, i + 1 as int).drop_last() =~= brackets@.subrange(0, i as int));
        // assert-end
        i += 1;
    }
    // assert-start
    assert(brackets@ =~= brackets@.subrange(0, i as int));
    // assert-end
    b && stack_size == 0
    // impl-end
}

} // verus!
fn main() {}
