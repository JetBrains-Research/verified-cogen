use vstd::prelude::*;

verus! {

fn filter_odd_numbers(arr: &Vec<u32>) -> (odd_list: Vec<u32>)
    // post-conditions-start
    ensures
        odd_list@ == arr@.filter(|x: u32| x % 2 != 0),
    // post-conditions-end
{
    // impl-start
    let mut odd_list: Vec<u32> = Vec::new();
    let input_len = arr.len();

    // assert-start
    assert(arr@.take(0int).filter(|x: u32| x % 2 != 0) == Seq::<u32>::empty());
    // assert-end
    let mut index = 0;
    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            odd_list@ == arr@.take(index as int).filter(|x: u32| x % 2 != 0),
        // invariants-end
    {
        if (arr[index] % 2 != 0) {
            odd_list.push(arr[index]);
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
    odd_list
    // impl-end
}

} // verus!

fn main() {}
