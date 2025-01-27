use vstd::prelude::*;

verus! {

fn extract_rear_chars(s: &Vec<Vec<char>>) -> (result: Vec<char>)
    // pre-conditions-start
    requires
        forall|i: int| 0 <= i < s.len() ==> #[trigger] s[i].len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        s.len() == result.len(),
        forall|i: int| 0 <= i < s.len() ==> result[i] == #[trigger] s[i][s[i].len() - 1],
    // post-conditions-end
{
    // impl-start
    let mut rear_chars: Vec<char> = Vec::with_capacity(s.len());
    let mut index = 0;
    while index < s.len()
        // invariants-start
        invariant
            0 <= index <= s.len(),
            rear_chars.len() == index,
            forall|i: int| 0 <= i < s.len() ==> #[trigger] s[i].len() > 0,
            forall|k: int| 0 <= k < index ==> rear_chars[k] == #[trigger] s[k][s[k].len() - 1],
        // invariants-end
    {
        let seq = &s[index];
        rear_chars.push(seq[seq.len() - 1]);
        index += 1;
    }
    rear_chars
    // impl-end
}

} // verus!

fn main() {}
