use vstd::prelude::*;

verus! {

fn max_array(nums: &[i32]) -> (idx: usize)
    requires
        nums.len() >= 1,
    ensures
        0 <= idx && idx < nums.len(),
        forall|i: int| 0 <= i && i < nums.len() ==> nums[i] <= nums[idx as int],
{
    let mut idx = 0;

    let mut i = 1;
    while i < nums.len()
        invariant
            0 < i <= nums.len(),
            0 <= idx && idx < i,
            forall|j: int| 0 <= j && j < i ==> nums[j] <= nums[idx as int],
    {
        if nums[i] > nums[idx] {
            idx = i;
        }
        i = i + 1;
    }
    idx
}

fn main() {}
}