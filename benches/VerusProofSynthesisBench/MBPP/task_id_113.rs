use vstd::prelude::*;

verus! {

spec fn is_digit_sepc(c: char) -> (res: bool) {
    (c as u32) >= 48 && (c as u32) <= 57
}
// pure-end

fn is_digit(c: char) -> (res: bool)
    // post-conditions-start
    ensures
        res == is_digit_sepc(c),
    // post-conditions-end
{
    (c as u32) >= 48 && (c as u32) <= 57
}

fn is_integer(text: &Vec<char>) -> (result: bool)
    // post-conditions-start
    ensures
        result == (forall|i: int| 0 <= i < text.len() ==> (#[trigger] is_digit_sepc(text[i]))),
    // post-conditions-end
{
    // impl-start
    let mut index = 0;
    while index < text.len()
        // invariants-start
        invariant
            0 <= index <= text.len(),
            forall|i: int| 0 <= i < index ==> (#[trigger] is_digit_sepc(text[i])),
        // invariants-end
    {
        if (!is_digit(text[index])) {
            return false;
        }
        index += 1;
    }
    true
    // impl-end
}

} // verus!

fn main() {}