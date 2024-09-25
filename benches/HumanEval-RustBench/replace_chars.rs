use vstd::prelude::*;

verus! {

fn replace_chars(s: &[char], old: char, new: char) -> (result: Vec<char>)
    // post-conditions-start
    ensures
        result.len() == s.len(),
        forall|i: int| 0 <= i && i < result.len() ==> result[i] == (if s[i] == old { new } else { s[i] }),
    // post-conditions-end
{
    // impl-start
    let mut result: Vec<char> = Vec::new();
    let mut i = 0;
    while i < s.len()
        // invariants-start
        invariant
            0 <= i && i <= s.len(),
            result.len() == i,
            forall|j: int| 0 <= j && j < i ==> result[j] == (if s[j] == old { new } else { s[j] }),
        // invariants-end
    {
        result.push(if s[i] == old { new } else { s[i] });
        i = i + 1;
    }
    result
    // impl-end
}

fn main() {}
}
