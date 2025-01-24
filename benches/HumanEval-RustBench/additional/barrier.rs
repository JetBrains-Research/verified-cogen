use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn barrier(arr: &[i32], p: usize) -> (result: bool)
    // pre-conditions-start
    requires
        arr.len() > 0,
        0 <= p < arr.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        result == forall|k: int, l: int| 0 <= k <= p && p < l < arr.len() ==> arr[k] < arr[l],
    // post-conditions-end
{
    // impl-start
    let mut i = 1;
    let mut max: usize = 0;
    while i <= p
        // invariants-start
        invariant
            0 <= i <= p + 1,
            0 <= max < i,
            forall|k: int| 0 <= k < i ==> arr[max as int] >= arr[k],
        // invariants-end
    {
        if arr[i] > arr[max] {
            max = i;
        }
        i = i + 1;
    }

    let mut result = true;
    while i < arr.len()
        // invariants-start
        invariant
            p < i <= arr.len(),
            forall|k: int| 0 <= k <= p ==> arr[max as int] >= arr[k],
            result == forall|k: int, l: int| 0 <= k <= p && p < l < i ==> arr[k] < arr[l],
        // invariants-end
    {
        if arr[max] >= arr[i] {
            result = false;
        }
        i = i + 1;
    }
    result
    // impl-end
}

fn main() {}
}
