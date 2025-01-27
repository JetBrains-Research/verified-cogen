use vstd::prelude::*;

verus! {

fn remove_odds(arr: &Vec<u32>) -> (even_list: Vec<u32>)
    // post-conditions-start
    ensures
        even_list@ == arr@.filter(|x: u32| x % 2 == 0),
    // post-conditions-end
{
    // impl-start
    let mut even_list: Vec<u32> = Vec::new();
    let input_len = arr.len();

    assert(arr@.take(0int).filter(|x: u32| x % 2 == 0) == Seq::<u32>::empty());
    let mut index = 0;
    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            even_list@ == arr@.take(index as int).filter(|x: u32| x % 2 == 0),
        // invariants-end
    {
        if (arr[index] % 2 == 0) {
            even_list.push(arr[index]);
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
    even_list
    // impl-end
}

} // verus!

fn main() {}
