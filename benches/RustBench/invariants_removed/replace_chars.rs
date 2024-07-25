use vstd::prelude::*;

verus! {

fn replace_chars(s: &[char], old: char, new: char) -> (result: Vec<char>)
    ensures
        result.len() == s.len(),
        forall|i: int| 0 <= i && i < result.len() ==> result[i] == (if s[i] == old { new } else { s[i] }),
{
    let mut result: Vec<char> = Vec::new();
    let mut i = 0;
    while i < s.len()
    {
        result.push(if s[i] == old { new } else { s[i] });
        i = i + 1;
    }
    result
}

fn main() {}
}