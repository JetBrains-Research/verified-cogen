use vstd::prelude::*;


verus! {

spec fn is_digit(c: char) -> (result: bool) {
    (c as u8) >= 48 && (c as u8) <= 57
}
// pure-end

spec fn count_digits_recursively(seq: Seq<char>) -> (result: int)
    decreases seq.len(),
{
    if seq.len() == 0 {
        0
    } else {
        count_digits_recursively(seq.drop_last()) + if is_digit(seq.last()) {
            1 as int
        } else {
            0 as int
        }
    }
}
// pure-end

fn count_digits(text: &Vec<char>) -> (count: usize)
    // pre-conditions-start
    ensures
        0 <= count <= text.len(),
        count_digits_recursively(text@) == count,
    // pre-conditions-end
{
    // impl-start
    let mut count = 0;

    let mut index = 0;
    while index < text.len()
        // invariants-start
        invariant
            0 <= index <= text.len(),
            0 <= count <= index,
            count == count_digits_recursively(text@.subrange(0, index as int)),
        // invariants-end
    {
        if ((text[index] as u8) >= 48 && (text[index] as u8) <= 57) {
            count += 1;
        }
        index += 1;
        // assert-start
        assert(text@.subrange(0, index - 1 as int) == text@.subrange(0, index as int).drop_last());
        // assert-end
    }
    // assert-start
    assert(text@ == text@.subrange(0, index as int));
    // assert-end
    count
    // impl-end
}

} // verus!

fn main() {}
