use vstd::prelude::*;
fn main() {}

verus! {

fn split_and_append(list: &Vec<i32>, n: usize) -> (new_list: Vec<i32>)
    // pre-conditions-start
    requires
        list@.len() > 0,
        0 < n < list@.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        new_list@ == list@.subrange(n as int, list@.len() as int).add(list@.subrange(0, n as int)),
    // post-conditions-end
{
    // impl-start
    let mut new_list = Vec::new();
    let mut index = n;
    while index < list.len()
        // invariants-start
        invariant
            n <= index <= list.len(),
            list@.subrange(n as int, index as int) =~= new_list@,
        // invariants-end
    {
        new_list.push(list[index]);
        index += 1;
    }
    let mut index = 0;
    while index < n
        // invariants-start
        invariant
            0 < n < list@.len(),
            0 <= index <= n,
            new_list@ =~= list@.subrange(n as int, list@.len() as int).add(
                list@.subrange(0, index as int),
            ),
        // invariants-end
    {
        new_list.push(list[index]);
        index += 1;
    }
    new_list
    // impl-end
}

} // verus!
