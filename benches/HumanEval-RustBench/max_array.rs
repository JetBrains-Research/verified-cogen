use vstd::prelude::*;

verus! {

fn max_array(nums: &[i32]) -> (idx: usize)
    // pre-conditions-start
    requires
        nums.len() >= 1,
    // pre-conditions-end
    // post-conditions-start
    ensures
        0 <= idx && idx < nums.len(),
        forall|i: int| 0 <= i && i < nums.len() ==> nums[i] <= nums[idx as int],
    // post-conditions-end
{
    // impl-start
    let mut idx = 0;

    let mut i = 1;
    while i < nums.len()
        // invariants-start
        invariant
            0 < i <= nums.len(),
            0 <= idx && idx < i,
            forall|j: int| 0 <= j && j < i ==> nums[j] <= nums[idx as int],
        // invariants-end
    {
        if nums[i] > nums[idx] {
            idx = i;
        }
        i = i + 1;
    }
    idx
    // impl-end
}

fn main() {}
}
