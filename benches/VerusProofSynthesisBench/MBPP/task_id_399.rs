use vstd::prelude::*;

fn main() {}

verus! {

fn bit_wise_xor(arr1: &Vec<i32>, arr2: &Vec<i32>) -> (result: Vec<i32>)
    // pre-conditions-start
    requires
        arr1.len() == arr2.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        result.len() == arr1.len(),
        forall|i: int|
            0 <= i < result.len() ==> result[i] == #[trigger] arr1[i] ^ #[trigger] arr2[i],
    // post-conditions-end
{
    // impl-start
    let mut output_arr = Vec::with_capacity(arr1.len());
    let mut index = 0;
    while index < arr1.len()
        // invariants-start
        invariant
            arr1.len() == arr2.len(),
            0 <= index <= arr2.len(),
            output_arr.len() == index,
            forall|k: int|
                0 <= k < index ==> output_arr[k] == #[trigger] arr1[k] ^ #[trigger] arr2[k],
        // invariants-end
    {
        output_arr.push((arr1[index] ^ arr2[index]));
        index += 1;
    }
    output_arr
    // impl-end
}

} // verus!
