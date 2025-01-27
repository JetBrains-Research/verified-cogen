use vstd::prelude::*;

verus! {

fn find_odd_numbers(arr: &Vec<u32>) -> (odd_numbers: Vec<u32>)
    // post-conditions-start
    ensures
        odd_numbers@ == arr@.filter(|x: u32| x % 2 != 0),
    // post-conditions-end
{
    // impl-start
    let mut odd_numbers: Vec<u32> = Vec::new();
    let input_len = arr.len();

    // assert-start
    assert(arr@.take(0int).filter(|x: u32| x % 2 != 0) == Seq::<u32>::empty());
    // assert-end
    let mut index = 0;
    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            odd_numbers@ == arr@.take(index as int).filter(|x: u32| x % 2 != 0),
        // invariants-end
    {
        if (arr[index] % 2 != 0) {
            odd_numbers.push(arr[index]);
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
    odd_numbers
    // impl-end
}

} // verus!

fn main() { }
