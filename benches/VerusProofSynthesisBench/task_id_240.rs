use vstd::prelude::*;

verus! {

fn replace_last_element(first: &Vec<i32>, second: &Vec<i32>) -> (replaced_list: Vec<i32>)
    // pre-conditions-start
    requires
        first.len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        replaced_list@ == first@.subrange(0, first.len() - 1).add(second@),
    // post-conditions-end
{
    // impl-start
    let mut replaced_list = Vec::new();
    let first_end = first.len() - 1;
    let mut index = 0;

    while index < first_end
        // invariants-start
        invariant
            first_end == first.len() - 1,
            0 <= index <= first_end,
            replaced_list@ =~= first@.subrange(0, index as int),
        // invariants-end
    {
        replaced_list.push(first[index]);
        index += 1;
    }
    index = 0;
    while index < second.len()
        // invariants-start
        invariant
            0 <= index <= second.len(),
            replaced_list@ =~= first@.subrange(0, first.len() - 1).add(
                second@.subrange(0, index as int),
            ),
        // invariants-end
    {
        replaced_list.push(second[index]);
        index += 1;
    }
    // assert-start
    assert(replaced_list@ =~= first@.subrange(0, first.len() - 1).add(second@));
    // assert-end
    replaced_list
    // impl-end
}

} // verus!


fn main() {}