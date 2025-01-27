
use vstd::prelude::*;

verus! {

spec fn is_upper_case(c: char) -> (result:bool) {
    c >= 'A' && c <= 'Z'
}
// pure-end

spec fn is_lower_case(c: char) -> (result:bool) {
    c >= 'a' && c <= 'z'
}
// pure-end

spec fn shift_plus_32_spec(c: char) -> (result:char) {
    ((c as u8) + 32) as char
}
// pure-end

spec fn shift_minus_32_spec(c: char) -> (result:char) {
    ((c as u8) - 32) as char
}
// pure-end

spec fn flip_case_spec(c: char) -> (result:char) {
    if is_lower_case(c) {
        shift_minus_32_spec(c)
    } else if is_upper_case(c) {
        shift_plus_32_spec(c)
    } else {
        c
    }
}
// pure-end

fn flip_case(str: &[char]) -> (flipped_case: Vec<char>)
    // post-conditions-start
    ensures
        str@.len() == flipped_case@.len(),
        forall|i: int| 0 <= i < str.len() ==> flipped_case[i] == flip_case_spec(#[trigger] str[i]),
    // post-conditions-end
{
    // impl-start
    let mut flipped_case = Vec::with_capacity(str.len());

    for index in 0..str.len()
        // invariants-start
        invariant
            0 <= index <= str.len(),
            flipped_case.len() == index,
            forall|i: int| 0 <= i < index ==> flipped_case[i] == flip_case_spec(#[trigger] str[i]),
        // invariants-end
    {
        if (str[index] >= 'a' && str[index] <= 'z') {
            flipped_case.push(((str[index] as u8) - 32) as char);
        } else if (str[index] >= 'A' && str[index] <= 'Z') {
            flipped_case.push(((str[index] as u8) + 32) as char);
        } else {
            flipped_case.push(str[index]);
        }
        // assert-start
        assert(flipped_case[index as int] == flip_case_spec(str[index as int]));
        // assert-end
    }
    flipped_case
    // impl-end
}

} // verus!
fn main() {}
