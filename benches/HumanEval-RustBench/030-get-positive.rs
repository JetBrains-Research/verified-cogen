use vstd::prelude::*;

verus! {

fn get_positive(input: Vec<i32>) -> (positive_list: Vec<i32>)
    // post-conditions-start
    ensures
        positive_list@ == input@.filter(|x: i32| x > 0),
    // post-conditions-end
{
    // impl-start
    let mut positive_list = Vec::<i32>::new();
    let input_len = input.len();
    assert(input@.take(0int).filter(|x: i32| x > 0) == Seq::<i32>::empty()); // assert-line
    for pos in 0..input_len
        // invariants-start
        invariant
            input_len == input.len(),
            positive_list@ == input@.take(pos as int).filter(|x: i32| x > 0),
        // invariants-end
    {
        let n = input[pos];
        if n > 0 {
            positive_list.push(n);
        }
        assert(input@.take((pos + 1) as int).drop_last() == input@.take(pos as int)); // assert-line
        reveal(Seq::filter);
    }
    assert(input@ == input@.take(input_len as int)); // assert-line
    positive_list
    // impl-end
}

}
fn main() {}
