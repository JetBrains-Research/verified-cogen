use vstd::prelude::*;


verus! {

fn square_nums(nums: &Vec<i32>) -> (squared: Vec<i32>)
    // pre-conditions-start
    requires
        forall|k: int|
            0 <= k < nums.len() ==> (0 <= #[trigger] nums[k] * #[trigger] nums[k] < i32::MAX),
    // pre-conditions-end
    // post-conditions-start
    ensures
        nums.len() == squared.len(),
        forall|k: int| 0 <= k < nums.len() ==> (#[trigger] squared[k] == nums[k] * nums[k]),
    // post-conditions-end
{
    // impl-start
    let mut result: Vec<i32> = Vec::new();
    let mut index = 0;

    while index < nums.len()
        // invariants-start
        invariant
            0 <= index <= nums.len(),
            result@.len() == index,
            forall|k: int|
                0 <= k < nums.len() ==> (0 <= #[trigger] nums[k] * #[trigger] nums[k] < i32::MAX),
            forall|k: int| 0 <= k < index ==> (#[trigger] result[k] == nums[k] * nums[k]),
        // invariants-end
    {
        result.push(nums[index] * nums[index]);
        index += 1
    }
    result
    // impl-end
}

} // verus!

fn main() {}
