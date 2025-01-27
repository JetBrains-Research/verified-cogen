use vstd::prelude::*;

verus! {

fn find_negative_numbers(arr: &Vec<i32>) -> (negative_list: Vec<i32>)
    // post-conditions-start
    ensures
        negative_list@ == arr@.filter(|x: i32| x < 0),
    // post-conditions-end
{
    // impl-start
    let mut negative_list: Vec<i32> = Vec::new();
    let input_len = arr.len();

    // assert-start
    assert(arr@.take(0int).filter(|x: i32| x < 0) == Seq::<i32>::empty());
    // assert-end
    let mut index = 0;
    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            negative_list@ == arr@.take(index as int).filter(|x: i32| x < 0),
        // invariants-end
    {
        if (arr[index] < 0) {
            negative_list.push(arr[index]);
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
    negative_list
    // impl-end
}

} // verus!

fn main() {}
