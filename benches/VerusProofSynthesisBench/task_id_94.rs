use vstd::prelude::*;


verus! {

fn min_second_value_first(arr: &Vec<Vec<i32>>) -> (first_of_min_second: i32)
    // pre-conditions-start
    requires
        arr.len() > 0,
        forall|i: int| 0 <= i < arr.len() ==> #[trigger] arr[i].len() >= 2,
    // pre-conditions-end
    // post-conditions-start
    ensures
        exists|i: int|
            0 <= i < arr.len() && first_of_min_second == #[trigger] arr[i][0] && (forall|j: int|
                0 <= j < arr.len() ==> (arr[i][1] <= #[trigger] arr[j][1])),
    // post-conditions-end
{
    // impl-start
    let mut min_second_index = 0;
    let mut index = 0;

    while index < arr.len()
        // invariants-start
        invariant
            0 <= min_second_index < arr.len(),
            forall|i: int| 0 <= i < arr.len() ==> #[trigger] arr[i].len() >= 2,
            forall|k: int|
                0 <= k < index ==> (arr[min_second_index as int][1] <= #[trigger] arr[k][1]),
        // invariants-end
    {
        // assert-start
        assert(arr[index as int].len() > 0);
        assert(arr[min_second_index as int].len() > 0);
        // assert-end

        if arr[index][1] < arr[min_second_index][1] {
            min_second_index = index;
        }
        index += 1;
    }
    // assert-start
    assert(arr[min_second_index as int].len() > 0);
    // assert-end
    arr[min_second_index][0]
    // impl-end
}

} // verus!

fn main() {}
