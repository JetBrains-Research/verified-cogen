use vstd::prelude::*;

fn main() {}

verus! {

fn interleave(s1: &Vec<i32>, s2: &Vec<i32>, s3: &Vec<i32>) -> (res: Vec<i32>)
    // pre-conditions-start
    requires
        s1@.len() == s2@.len() && s2@.len() == s3@.len(),
        0 <= (s1@.len() * 3) <= i32::MAX,
    // pre-conditions-end
    // post-conditions-start
    ensures
        res@.len() == s1@.len() * 3,
        forall|i: int|
            0 <= i < s1@.len() ==> (res[3 * i] == s1[i] && res[3 * i + 1] == s2[i] && res[3 * i + 2]
                == s3[i]),
    // post-conditions-end
{
    // impl-start
    let new_seq_len = s1.len() * 3;
    let mut output_seq = Vec::with_capacity(new_seq_len);
    let mut index = 0;

    while index < s1.len()
        // invariants-start
        invariant
            0 <= index <= s1.len(),
            output_seq@.len() == 3 * index,
            s1@.len() == s2@.len() && s2@.len() == s3@.len(),
            forall|k: int|
                0 <= k < index ==> (output_seq[3 * k] == s1[k] && output_seq[3 * k + 1] == s2[k]
                    && output_seq[3 * k + 2] == s3[k]),
        // invariants-end
    {
        output_seq.push(s1[index]);
        output_seq.push(s2[index]);
        output_seq.push(s3[index]);
        index += 1;
    }
    output_seq
    // impl-end
}

} // verus!
