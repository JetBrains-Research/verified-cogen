#[allow(unused_imports)]
use vstd::prelude::*;


verus! {
fn linear_search(nums: Vec<i32>, target: i32) -> (ret: i32)
    // pre-conditions-start
    requires
        nums@.len() < 0x8000_0000,
    // pre-conditions-end
    // post-conditions-start
    ensures
        ret < nums@.len(),
        ret >=0 ==> nums@[ret as int] == target,
        ret >=0 ==> forall |i: int| 0 <= i < ret as int ==> #[trigger]nums@[i]!= target,
        ret < 0 ==> forall |i: int| 0 <= i < nums@.len() as int ==> #[trigger]nums@[i] != target,
    // post-conditions-end
{
    // impl-start
    let mut i = 0;
    while i < nums.len()
        // invariants-start
        invariant
            forall |k: int| 0 <= k < i ==> #[trigger]nums[k]@!= target,
            0 <= i <= nums@.len(),
        ensures
            0 <= i < nums@.len() ==> (#[trigger]nums@[i as int]) == target,
        // invariants-end
    {
        if nums[i] == target {
            break;
        }
        i = i + 1;
    }
    if i == nums.len() {
        -1
    } else {
        i as i32
    }
    // impl-end
}
}

fn main() {}

