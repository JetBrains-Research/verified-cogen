use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn binary_search(arr: &[i32], target: i32) -> (result: Option<usize>)
    // pre-conditions-start
    requires
        forall|i: int, j: int| 0 <= i && i < j && j < arr.len() ==> arr[i] <= arr[j],
    // pre-conditions-end
    // post-conditions-start
    ensures
        match result {
            Some(index) => arr[index as int] == target && arr.len() > 0 && index < arr.len(),
            None => forall|i: int| 0 <= i && i < arr.len() ==> arr[i] != target,
        },
    // post-conditions-end
{
    // impl-start
    let mut low = 0;
    let mut high = arr.len();
    while low < high
        // invariants-start
        invariant
            low <= high && high <= arr.len(),
            forall|i: int| 0 <= i && i < low ==> arr[i] < target,
            forall|i: int| high <= i && i < arr.len() ==> arr[i] > target,
        // invariants-end
    {
        let mid = low + (high - low) / 2;
        if arr[mid] == target {
            return Some(mid);
        } else if arr[mid] < target {
            low = mid;
        } else {
            high = mid;
        }
    }
    None
    // impl-end
}

fn main() {}
}
