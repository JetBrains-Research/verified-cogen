use vstd::prelude::*;

verus! {

spec fn is_lower_case(c: char) -> (result: bool) {
    c >= 'a' && c <= 'z'
}
// pure-end

spec fn shift_minus_32_spec(c: char) -> (result: char) {
    ((c as u8) - 32) as char
}
// pure-end

spec fn inner_expr_to_uppercase(str1: &Vec<char>, i: int) -> (result:char) {
    if is_lower_case(#[trigger] str1[i]) {
        shift_minus_32_spec(str1[i])
    } else {
        str1[i]
    }
}

fn to_uppercase(str1: &Vec<char>) -> (result: Vec<char>)
    // post-conditions-start
    ensures
        str1@.len() == result@.len(),
        forall|i: int|
            0 <= i < str1.len() ==> (result[i] == (inner_expr_to_uppercase(str1, i))),
    // post-conditions-end
{
    // impl-start
    let mut upper_case: Vec<char> = Vec::with_capacity(str1.len());
    let mut index = 0;
    while index < str1.len()
        // invariants-start
        invariant
            0 <= index <= str1.len(),
            upper_case.len() == index,
            forall|i: int|
                0 <= i < index ==> (upper_case[i] == (if is_lower_case(#[trigger] str1[i]) {
                    shift_minus_32_spec(str1[i])
                } else {
                    str1[i]
                })),
        // invariants-end
    {
        if (str1[index] >= 'a' && str1[index] <= 'z') {
            upper_case.push(((str1[index] as u8) - 32) as char);
        } else {
            upper_case.push(str1[index]);
        }
        // assert-start
        assert(upper_case[index as int] == (if is_lower_case(str1[index as int]) {
            shift_minus_32_spec(str1[index as int])
        } else {
            str1[index as int]
        }));
        // assert-end
        index += 1;
    }
    // assert-start
    assert(forall|i: int|
        0 <= i < str1.len() ==> upper_case[i] == (if is_lower_case(#[trigger] str1[i]) {
            shift_minus_32_spec(str1[i])
        } else {
            str1[i]
        }));
    // assert-end
    upper_case
    // impl-end
}

} // verus!

fn main() {}

