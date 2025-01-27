use vstd::prelude::*;


verus! {

spec fn check_find_first_odd(arr: &Vec<u32>, index: Option<usize>) -> (result: bool)
{
    if let Some(idx) = index {
        &&& arr@.take(idx as int) == arr@.take(idx as int).filter(|x: u32| x % 2 == 0)
        &&& arr[idx as int] % 2 != 0
    } else {
        forall|k: int| 0 <= k < arr.len() ==> (arr[k] % 2 == 0)
    }
}
// pure-end

fn find_first_odd(arr: &Vec<u32>) -> (index: Option<usize>)
    // post-conditions-start
    ensures check_find_first_odd(arr, index),
    // post-conditions-end
{
    // impl-start
    let input_len = arr.len();
    let mut index = 0;
    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            arr@.take(index as int) =~= arr@.take(index as int).filter(|x: u32| x % 2 == 0),
        // invariants-end
    {
        if (arr[index] % 2 != 0) {
            return Some(index);
        }
        // assert-start
        assert(arr@.take((index + 1) as int).drop_last() == arr@.take(index as int));
        reveal(Seq::filter);
        // assert-end
        index += 1;
    }
    // assert-start
    assert(arr@ == arr@.take(input_len as int));
    // assert-end
    None
    // impl-end
}

} // verus!

fn main() {}