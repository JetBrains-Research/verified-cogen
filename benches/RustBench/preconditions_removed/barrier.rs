#![crate_name="barrier"]

use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn barrier(arr: &[i32], p: usize) -> (result: bool)
    ensures
        result == forall|k: int, l: int| 0 <= k <= p && p < l < arr.len() ==> arr[k] < arr[l],
{
    let mut i = 1;
    let mut max: usize = 0;
    while i <= p
        invariant
            0 <= i <= p + 1,
            0 <= max < i,
            forall|k: int| 0 <= k < i ==> arr[max as int] >= arr[k],
    {
        if arr[i] > arr[max] {
            max = i;
        }
        i = i + 1;
    }

    let mut result = true;
    while i < arr.len()
        invariant
            p < i <= arr.len(),
            forall|k: int| 0 <= k <= p ==> arr[max as int] >= arr[k],
            result == forall|k: int, l: int| 0 <= k <= p && p < l < i ==> arr[k] < arr[l],
    {
        if arr[max] >= arr[i] {
            result = false;
        }
        i = i + 1;
    }
    result
}

fn main() {}
}
