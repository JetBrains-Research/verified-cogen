use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn pairs_sum_to_zero(nums: &[i32], target: i32) -> (found: bool)
    // pre-conditions-start
    requires
        nums.len() >= 2,
        forall|i: int, j: int|
            0 <= i < j < nums.len() ==> nums[i] + nums[j] <= i32::MAX && nums[i] + nums[j]
                >= i32::MIN,
    // pre-conditions-end
    // post-conditions-start
    ensures
        found <==> exists|i: int, j: int| 0 <= i < j < nums.len() && nums[i] + nums[j] == target,
    // post-conditions-end
{
    // impl-start
    let mut i = 0;

    while i < nums.len()
        // invariants-start
        invariant
            0 <= i <= nums.len(),
            forall|u: int, v: int| 0 <= u < v < nums.len() && u < i ==> nums[u] + nums[v] != target,
        // invariants-end
    {
        let mut j = i + 1;
        while j < nums.len()
            // invariants-start
            invariant
                0 <= i < j <= nums.len(),
                forall|u: int, v: int|
                    0 <= u < v < nums.len() && u < i ==> nums[u] + nums[v] != target,
                forall|u: int| i < u < j ==> nums[i as int] + nums[u] != target,
            // invariants-end
        {
            if nums[i] + nums[j] == target {
                return true;
            }
            j = j + 1;
        }
        i = i + 1;
    }
    false
    // impl-end
}

}
fn main() {}
