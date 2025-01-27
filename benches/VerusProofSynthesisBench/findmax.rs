#[allow(unused_imports)]
use vstd::prelude::*;

verus! {
fn find_max(nums: Vec<i32>) -> (ret:i32)
    // pre-conditions-start
    requires
        nums.len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        forall |i: int| 0 <= i < nums@.len() ==> nums@[i] <= ret,
        exists |i: int| 0 <= i < nums@.len() ==> nums@[i] == ret,
    // post-conditions-end
{
    // impl-start
    let mut max = nums[0];
    let mut i = 1;
    while i < nums.len()
        // invariants-start
        invariant
            forall |k: int| 0 <= k < i ==> nums@[k] <= max,
            exists |k: int| 0 <= k < i && nums@[k] == max,
        // invariants-end
    {
        if nums[i] > max {
            max = nums[i];
        }
        i += 1;
    }
    max
    // impl-end
}
}


fn main() {}