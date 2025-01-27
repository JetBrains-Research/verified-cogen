use vstd::prelude::*;

verus! {

fn cube_element(nums: &Vec<i32>) -> (cubed: Vec<i32>)
    // pre-conditions-start
    requires
        forall|k: int|
            0 <= k < nums.len() ==> (i32::MIN <= #[trigger] nums[k] * #[trigger] nums[k]
                <= i32::MAX),
        forall|k: int|
            0 <= k < nums.len() ==> (i32::MIN <= #[trigger] nums[k] * #[trigger] nums[k]
                * #[trigger] nums[k] <= i32::MAX),
    // pre-conditions-end
    // post-conditions-start
    ensures
        forall|i: int|
            0 <= i < nums.len() ==> cubed[i] == #[trigger] nums[i] * #[trigger] nums[i]
                * #[trigger] nums[i],
    // post-conditions-end
{
    // impl-start
    let mut cubed_array: Vec<i32> = Vec::new();
    let mut i = 0;
    while i < nums.len()
        // invariants-start
        invariant
            cubed_array@.len() == i,
            forall|k: int|
                0 <= k < nums.len() ==> (i32::MIN <= #[trigger] nums[k] * #[trigger] nums[k]
                    <= i32::MAX),
            forall|k: int|
                0 <= k < nums.len() ==> (i32::MIN <= #[trigger] nums[k] * #[trigger] nums[k]
                    * #[trigger] nums[k] <= i32::MAX),
            forall|k: int|
                0 <= k < i ==> (#[trigger] cubed_array[k] == nums[k] * nums[k] * nums[k]),
        // invariants-end
    {
        cubed_array.push(nums[i] * nums[i] * nums[i]);
        i += 1;
    }
    cubed_array
    // impl-end
}

} // verus!

fn main() {}

