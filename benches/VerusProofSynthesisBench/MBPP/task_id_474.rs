use vstd::prelude::*;

verus! {

spec fn inner_epxr_replace_chars(str1: &Vec<char>, old_char: char, new_char: char, i: int) -> (result: char) {
    if str1[i] == old_char {
        new_char
    } else {
        str1[i]
    }
}
// pure-end

fn replace_chars(str1: &Vec<char>, old_char: char, new_char: char) -> (result: Vec<char>)
    // post-conditions-start
    ensures
        str1@.len() == result@.len(),
        forall|i: int|
            0 <= i < str1.len() ==> result[i] == inner_epxr_replace_chars(str1, old_char, new_char, i),
    // post-conditions-end
{
    // impl-start
    let mut result_str = Vec::with_capacity(str1.len());
    let mut index = 0;
    while index < str1.len()
        // invariants-start
        invariant
            0 <= index <= str1@.len(),
            result_str@.len() == index,
            forall|k: int|
                0 <= k < index ==> result_str[k] == (if str1[k] == old_char {
                    new_char
                } else {
                    str1[k]
                }),
        // invariants-end
    {
        if str1[index] == old_char {
            result_str.push(new_char);
        } else {
            result_str.push(str1[index]);
        }
        index += 1;
    }
    result_str
    // impl-end
}

} // verus!

fn main() {}
