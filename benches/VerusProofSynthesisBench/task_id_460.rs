use vstd::prelude::*;

verus! {

fn get_first_elements(arr: &Vec<Vec<i32>>) -> (result: Vec<i32>)
    // pre-conditions-start
    requires
        forall|i: int| 0 <= i < arr.len() ==> #[trigger] arr[i].len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        arr.len() == result.len(),
        forall|i: int| 0 <= i < arr.len() ==> #[trigger] result[i] == #[trigger] arr[i][0],
    // post-conditions-end
{
    // impl-start
    let mut first_elem_arr: Vec<i32> = Vec::new();
    let mut index = 0;
    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            first_elem_arr.len() == index,
            forall|i: int| 0 <= i < arr.len() ==> #[trigger] arr[i].len() > 0,
            forall|k: int| 0 <= k < index ==> #[trigger] first_elem_arr[k] == #[trigger] arr[k][0],
        // invariants-end
    {
        let seq = &arr[index];
        // assert-start
        assert(seq.len() > 0);
        // assert-end
        first_elem_arr.push(seq[0]);
        index += 1;
    }
    first_elem_arr
    // impl-end
}

} // verus!

fn main() {}
