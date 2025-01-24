use vstd::prelude::*;

verus! {

spec fn count_frequency_spec(seq: Seq<i64>, key: i64) -> (result:int)
    decreases seq.len(),
{
    if seq.len() == 0 {
        0
    } else {
        count_frequency_spec(seq.drop_last(), key) + if (seq.last() == key) {
            1 as int
        } else {
            0 as int
        }
    }
}
// pure-end

fn count_frequency(elements: &Vec<i64>, key: i64) -> (frequency: usize)
    // post-conditions-start
    ensures
        count_frequency_spec(elements@, key) == frequency,
    // post-conditions-end
{
    // impl-start
    let ghost elements_length = elements.len();
    let mut counter = 0;
    let mut index = 0;
    while index < elements.len()
        // invariants-start
        invariant
            0 <= index <= elements.len(),
            0 <= counter <= index,
            count_frequency_spec(elements@.subrange(0, index as int), key) == counter,
        // invariants-end
    {
        if (elements[index] == key) {
            counter += 1;
        }
        index += 1;
        // assert-start
        assert(elements@.subrange(0, index - 1 as int) == elements@.subrange(
            0,
            index as int,
        ).drop_last());
        // assert-end
    }
    // assert-start
    assert(elements@ == elements@.subrange(0, elements_length as int));
    // assert-end
    counter
    // impl-end
}

fn remove_duplicates(numbers: &Vec<i64>) -> (unique_numbers: Vec<i64>)
    // post-conditions-start
    ensures
        unique_numbers@ == numbers@.filter(|x: i64| count_frequency_spec(numbers@, x) == 1),
    // post-conditions-end
{
    // impl-start
    let ghost numbers_length = numbers.len();
    let mut unique_numbers: Vec<i64> = Vec::new();
    // assert-start
    assert(numbers@.take(0int).filter(|x: i64| count_frequency_spec(numbers@, x) == 1) == Seq::<
        i64,
    >::empty());
    // assert-end

    for index in 0..numbers.len()
        // invariants-start
        invariant
            0 <= index <= numbers.len(),
            unique_numbers@ == numbers@.take(index as int).filter(
                |x: i64| count_frequency_spec(numbers@, x) == 1,
            ),
        // invariants-end
    {
        if count_frequency(&numbers, numbers[index]) == 1 {
            unique_numbers.push(numbers[index]);
        }
        // assert-start
        assert(numbers@.take((index + 1) as int).drop_last() == numbers@.take(index as int));
        // assert-end
        reveal(Seq::filter);
    }
    // assert-start
    assert(numbers@ == numbers@.take(numbers_length as int));
    // assert-end
    unique_numbers
    // impl-end
}

} // verus!
fn main() {}