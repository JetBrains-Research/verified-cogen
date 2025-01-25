use vstd::prelude::*;

fn main() {}

verus! {

fn smallest_list_length(list: &Vec<Vec<i32>>) -> (min: usize)
    // pre-conditions-start
    requires
        list.len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        min >= 0,
        forall|i: int| 0 <= i < list.len() ==> min <= #[trigger] list[i].len(),
        exists|i: int| 0 <= i < list.len() && min == #[trigger] list[i].len(),
    // post-conditions-end
{
    // impl-start
    let mut min = list[0].len();

    let mut index = 1;
    while index < list.len()
        // invariants-start
        invariant
            0 <= index <= list.len(),
            forall|k: int| 0 <= k < index ==> min <= #[trigger] list[k].len(),
            exists|k: int| 0 <= k < index && min == #[trigger] list[k].len(),
        // invariants-end
    {
        if (&list[index]).len() < min {
            min = (&list[index]).len();
        }
        index += 1;
    }
    min
    // impl-end
}

} // verus!
