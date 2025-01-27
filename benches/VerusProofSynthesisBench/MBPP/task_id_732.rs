use vstd::prelude::*;

verus! {

spec fn is_space_comma_dot_spec(c: char) -> (result: bool) {
    (c == ' ') || (c == ',') || (c == '.')
}
// pure-end

spec fn inner_expr_replace_with_colon(str1: &Vec<char>, k: int) -> (result: char) {
    if is_space_comma_dot_spec(str1[k]) {
        ':'
    } else {
        str1[k]
    }
}
// pure-end

fn replace_with_colon(str1: &Vec<char>) -> (result: Vec<char>)
    // post-conditions-start
    ensures
        str1@.len() == result@.len(),
        forall|k: int|
            0 <= k < result.len() ==> #[trigger] result[k] == inner_expr_replace_with_colon(str1, k),
    // post-conditions-end
{
    // impl-start
    let mut result: Vec<char> = Vec::with_capacity(str1.len());
    let mut index = 0;
    while index < str1.len()
        // invariants-start
        invariant
            0 <= index <= str1.len(),
            result@.len() == index,
            forall|k: int|
                0 <= k < index ==> #[trigger] result[k] == (if is_space_comma_dot_spec(str1[k]) {
                    ':'
                } else {
                    str1[k]
                }),
        // invariants-end
    {
        if ((str1[index] == ' ') || (str1[index] == ',') || (str1[index] == '.')) {
            result.push(':');
        } else {
            result.push(str1[index]);
        }
        index += 1;
    }
    result
    // impl-end
}

} // verus!

fn main() {}
