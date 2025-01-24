use vstd::prelude::*;

verus! {


spec fn extract_first_digit_spec(n: int) -> (ret:int)
    decreases n,
{
    if n < 10 {
        n
    } else {
        extract_first_digit_spec(n / 10)
    }
}
// pure-end

fn extract_first_digit(n: u32) -> (res: u32)
    // post-conditions-start
    ensures
        res == extract_first_digit_spec(n as int),
    // post-conditions-end
{
    // impl-start
    if n < 10 {
        n
    } else {
        extract_first_digit(n / 10)
    }
    // impl-end
}


spec fn extract_last_digit_spec(n: int) -> (ret:int) {
    n % 10
}
// pure-end

fn extract_last_digit(n: u32) -> (res: u32)
    // post-conditions-start
    ensures
        res == extract_last_digit_spec(n as int),
    // post-conditions-end
{
    // impl-start
    n % 10
    // impl-end
}

spec fn is_odd(n: int) -> (ret:bool) {
    (n % 2) != 0
}
// pure-end


spec fn is_valid_element_spec(n: int) -> (ret:bool) {
    &&& (n > 10)
    &&& is_odd(extract_first_digit_spec(n))
    &&& is_odd(extract_last_digit_spec(n))
}
// pure-end

fn is_valid_element(n: i32) -> (res: bool)
    // post-conditions-start
    ensures
        res == is_valid_element_spec(n as int),
    // post-conditions-end
{
    // impl-start
    ((n > 10) && (extract_first_digit(n as u32) % 2 != 0) && (extract_last_digit(n as u32) % 2
        != 0))
    // impl-end
}


spec fn special_filter_spec(seq: Seq<i32>) -> (ret:int)
    decreases seq.len(),
{
    if seq.len() == 0 {
        0
    } else {
        special_filter_spec(seq.drop_last()) + if (is_valid_element_spec(seq.last() as int)) {
            1 as int
        } else {
            0 as int
        }
    }
}
// pure-end

fn special_filter(numbers: &Vec<i32>) -> (count: usize)
    // post-conditions-start
    ensures
        count == special_filter_spec(numbers@),
    // post-conditions-end
{
    // impl-start
    let ghost numbers_length = numbers.len();
    let mut counter: usize = 0;
    let mut index = 0;
    while index < numbers.len()
        // invariants-start
        invariant
            0 <= index <= numbers.len(),
            0 <= counter <= index,
            counter == special_filter_spec(numbers@.subrange(0, index as int)),
        // invariants-end
    {
        if (is_valid_element(numbers[index])) {
            counter += 1;
        }
        index += 1;
        // assert-start
        assert(numbers@.subrange(0, index - 1 as int) == numbers@.subrange(
            0,
            index as int,
        ).drop_last());
        // assert-end
    }
    assert(numbers@ == numbers@.subrange(0, numbers_length as int)); // assert-line
    counter
    // impl-end
}

} // verus!
fn main() {}
