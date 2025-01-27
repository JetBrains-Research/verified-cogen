use vstd::prelude::*;

verus! {

fn remove_kth_element(list: &Vec<i32>, k: usize) -> (new_list: Vec<i32>)
    // pre-conditions-start
    requires
        list.len() > 0,
        0 < k < list@.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        new_list@ == list@.subrange(0, k - 1 as int).add(
            list@.subrange(k as int, list.len() as int),
        ),
    // post-conditions-end
{
    // impl-start
    let mut new_list = Vec::new();
    let mut index = 0;
    while index < (k - 1)
        // invariants-start
        invariant
            0 <= index <= k - 1,
            0 < k < list@.len(),
            new_list@ =~= list@.subrange(0, index as int),
        // invariants-end
    {
        new_list.push(list[index]);
        index += 1;
    }
    let mut index = k;
    while index < list.len()
        // invariants-start
        invariant
            k <= index <= list.len(),
            new_list@ =~= list@.subrange(0 as int, k - 1 as int).add(
                list@.subrange(k as int, index as int),
            ),
        // invariants-end
    {
        new_list.push(list[index]);
        index += 1;
    }
    // assert-start
    assert(new_list@ == list@.subrange(0, k - 1 as int).add(
        list@.subrange(k as int, list.len() as int),
    ));
    // assert-end
    new_list
    // impl-end
}

} // verus!

fn main() {}

