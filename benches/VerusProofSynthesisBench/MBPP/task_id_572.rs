use vstd::prelude::*;

verus! {

spec fn count_frequency_rcr(seq: Seq<i32>, key: i32) -> (result: int)
    decreases seq.len(),
{
    if seq.len() == 0 {
        0
    } else {
        count_frequency_rcr(seq.drop_last(), key) + if (seq.last() == key) {
            1 as int
        } else {
            0 as int
        }
    }
}
// pure-end

fn count_frequency(arr: &Vec<i32>, key: i32) -> (frequency: usize)
    // post-conditions-start
    ensures
        count_frequency_rcr(arr@, key) == frequency,
    // post-conditions-end
{
    // impl-start
    let mut index = 0;
    let mut counter = 0;
    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            0 <= counter <= index,
            count_frequency_rcr(arr@.subrange(0, index as int), key) == counter,
        // invariants-end
    {
        if (arr[index] == key) {
            counter += 1;
        }
        index += 1;
        // assert-start
        assert(arr@.subrange(0, index - 1 as int) == arr@.subrange(0, index as int).drop_last());
        // assert-end
    }
    // assert-start
    assert(arr@ == arr@.subrange(0, index as int));
    // assert-end
    counter
    // impl-end
}

fn remove_duplicates(arr: &Vec<i32>) -> (unique_arr: Vec<i32>)
    // post-conditions-start
    ensures
        unique_arr@ == arr@.filter(|x: i32| count_frequency_rcr(arr@, x) == 1),
    // post-conditions-end
{
    // impl-start
    let mut unique_arr: Vec<i32> = Vec::new();
    let input_len = arr.len();

    // assert-start
    assert(arr@.take(0int).filter(|x: i32| count_frequency_rcr(arr@, x) == 1) == Seq::<
        i32,
    >::empty());
    // assert-end

    let mut index = 0;
    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            unique_arr@ == arr@.take(index as int).filter(
                |x: i32| count_frequency_rcr(arr@, x) == 1,
            ),
        // invariants-end
    {
        if count_frequency(&arr, arr[index]) == 1 {
            unique_arr.push(arr[index]);
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
    unique_arr
    // impl-end
}

} // verus!

fn main() {}
