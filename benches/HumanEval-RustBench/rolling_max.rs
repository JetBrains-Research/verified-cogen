use vstd::prelude::*;

verus! {

spec fn seq_max(a: Seq<i32>) -> i32
    decreases a.len(),
{
    if a.len() == 0 {
        i32::MIN
    } else if a.last() > seq_max(a.drop_last()) {
        a.last()
    } else {
        seq_max(a.drop_last())
    }
}

fn rolling_max(numbers: Vec<i32>) -> (result: Vec<i32>)
    // post-conditions-start
    ensures
        result.len() == numbers.len(),
        forall|i: int| 0 <= i < numbers.len() ==> result[i] == seq_max(numbers@.take(i + 1)),
    // post-conditions-end
{
    // impl-start
    let mut max_so_far = i32::MIN;
    let mut result = Vec::with_capacity(numbers.len());
    let mut pos = 0;
    while pos < numbers.len()
        // invariants-start
        invariant
            0 <= pos <= numbers.len(),
            result.len() == pos,
            max_so_far == seq_max(numbers@.take(pos as int)),
            forall|i: int| 0 <= i < pos ==> result[i] == seq_max(numbers@.take(i + 1)),
            pos < numbers.len() ==> numbers@.take((pos + 1) as int).drop_last() =~= numbers@.take(pos as int)
        // invariants-end
    {
        let number = numbers[pos];
        if number > max_so_far {
            max_so_far = number;
        }
        result.push(max_so_far);
        pos += 1;
    }
    result
    // impl-end
}

fn main() {}
}
