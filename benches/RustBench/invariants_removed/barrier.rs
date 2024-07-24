use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn barrier(arr: &[i32], p: usize) -> (result: bool)
    requires
        arr.len() > 0,
        0 <= p < arr.len(),
    ensures
        result == forall|k: int, l: int| 0 <= k <= p && p < l < arr.len() ==> arr[k] < arr[l],
{
    let mut i = 1;
    let mut max: usize = 0;
    while i <= p
    {
        if arr[i] > arr[max] {
            max = i;
        }
        i = i + 1;
    }

    let mut result = true;
    while i < arr.len()
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
