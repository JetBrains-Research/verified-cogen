use vstd::prelude::*;

verus! {

fn contains(arr: &Vec<i32>, key: i32) -> (result: bool)
    // post-conditions-start
    ensures
        result == (exists|i: int| 0 <= i < arr.len() && (arr[i] == key)),
    // post-conditions-end
{
    // impl-start
    let mut i = 0;
    while i < arr.len()
        // invariants-start
        invariant
            forall|m: int| 0 <= m < i ==> (arr[m] != key),
        // invariants-end
    {
        if (arr[i] == key) {
            return true;
        }
        i += 1;
    }
    false
    // impl-end
}

fn shared_elements(list1: &Vec<i32>, list2: &Vec<i32>) -> (shared: Vec<i32>)
    // post-conditions-start
    ensures
        forall|i: int|
            0 <= i < shared.len() ==> (list1@.contains(#[trigger] shared[i]) && list2@.contains(
                #[trigger] shared[i],
            )),
        forall|i: int, j: int| 0 <= i < j < shared.len() ==> shared[i] != shared[j],
    // post-conditions-end
{
    // impl-start
    let mut shared = Vec::new();
    let ghost mut shared_arr_len: int = 0;

    let mut index = 0;
    while index < list1.len()
        // invariants-start
        invariant
            forall|i: int|
                0 <= i < shared.len() ==> (list1@.contains(#[trigger] shared[i]) && list2@.contains(
                    #[trigger] shared[i],
                )),
            forall|m: int, n: int| 0 <= m < n < shared.len() ==> shared[m] != shared[n],
        // invariants-end
    {
        if (contains(list2, list1[index]) && !contains(&shared, list1[index])) {
            shared.push(list1[index]);
            // assert-start
            proof {
                shared_arr_len = shared_arr_len + 1;
            }
            // assert-end
        }
        index += 1
    }
    shared
    // impl-end
}

} // verus!

fn main() {}