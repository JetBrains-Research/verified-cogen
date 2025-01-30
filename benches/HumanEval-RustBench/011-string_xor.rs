use vstd::prelude::*;
use vstd::slice::*;

verus! {
spec fn is_binary_digit(c: char) -> (ret: bool) {
    c == '0' || c == '1'
}
// pure-end

spec fn xor_char(a: char, b: char) -> (result: char)
    recommends
        is_binary_digit(a),
        is_binary_digit(b),
{
    if a == b {
        '0'
    } else {
        '1'
    }
}
// pure-end

fn string_xor(a: &[char], b: &[char]) -> (result: Vec<char>)
    // pre-conditions-start
    requires
        a@.len() == b@.len(),
        forall|i: int| 0 <= i < a@.len() as int ==> is_binary_digit(#[trigger] a[i]),
        forall|i: int| 0 <= i < b@.len() as int ==> is_binary_digit(#[trigger] b[i]),
    // pre-conditions-end
    // post-conditions-start
    ensures
        result.len() == a@.len(),
        forall|i: int|
            0 <= i < result.len() as int ==> #[trigger] result[i] == xor_char(a[i], b[i]),
    // post-conditions-end
{
    // impl-start
    let a_len = a.len();
    let mut result = Vec::with_capacity(a_len);
    #[verifier::loop_isolation(false)]
    for pos in 0..a_len
        // invariants-start
        invariant
            result.len() == pos,
            forall|i: int| 0 <= i < pos ==> #[trigger] result[i] == xor_char(a[i], b[i]),
        // invariants-end
    {
        if *slice_index_get(a, pos) == *slice_index_get(b, pos) {
            result.push('0');
        } else {
            result.push('1');
        }
    }
    result
    // impl-end
}

}
fn main() {}
