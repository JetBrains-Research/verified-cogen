use vstd::prelude::*;

verus! {

spec fn is_upper_case(c: char) -> (result:bool) {
    c >= 'A' && c <= 'Z'
}
// pure-end

spec fn shift32_spec(c: char) -> (result:char) {
    ((c as u8) + 32) as char
}
// pure-end

spec fn is_lower_case(c: char) -> (result:bool) {
    c >= 'a' && c <= 'z'
}
// pure-end

spec fn shift_minus_32_spec(c: char) -> (result:char) {
    ((c as u8) - 32) as char
}
// pure-end

spec fn to_toggle_case_spec(s: char) -> (result:char) {
    if is_lower_case(s) {
        shift_minus_32_spec(s)
    } else if is_upper_case(s) {
        shift32_spec(s)
    } else {
        s
    }
}
// pure-end

fn to_toggle_case(str1: &Vec<char>) -> (toggle_case: Vec<char>)
    // post-conditions-start
    ensures
        str1@.len() == toggle_case@.len(),
        forall|i: int|
            0 <= i < str1.len() ==> toggle_case[i] == to_toggle_case_spec(#[trigger] str1[i]),
    // post-conditions-end
{
    // impl-start
    let mut toggle_case = Vec::with_capacity(str1.len());

    let mut index = 0;
    while index < str1.len()
        // invariants-start
        invariant
            0 <= index <= str1.len(),
            toggle_case.len() == index,
            forall|i: int|
                0 <= i < index ==> toggle_case[i] == to_toggle_case_spec(#[trigger] str1[i]),
        // invariants-end
    {
        if (str1[index] >= 'a' && str1[index] <= 'z') {
            toggle_case.push(((str1[index] as u8) - 32) as char);
        } else if (str1[index] >= 'A' && str1[index] <= 'Z') {
            toggle_case.push(((str1[index] as u8) + 32) as char);
        } else {
            toggle_case.push(str1[index]);
        }
        index += 1;
    }
    // assert-start
    assert(forall|i: int|
        0 <= i < str1.len() ==> toggle_case[i] == to_toggle_case_spec(#[trigger] str1[i]));
    // assert-end
    toggle_case
    // impl-end
}

} // verus!

fn main() {}
