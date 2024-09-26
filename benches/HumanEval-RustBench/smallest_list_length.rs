use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn smallest_list_length(lists: Vec<Vec<i32>>) -> (result: usize)
    // pre-conditions-start
    requires
        lists.len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        exists|i: int| #![auto] 0 <= i < lists.len() && result == lists[i].len(),
        forall|i: int| #![auto] 0 <= i < lists.len() ==> result <= lists[i].len(),
    // post-conditions-end
{
    // impl-start
    let mut result = lists[0].len();
    let mut i = 1;
    while i < lists.len()
        // invariants-start
        invariant
            0 <= i <= lists.len(),
            forall|j: int| #![auto] 0 <= j < i ==> result <= lists[j].len(),
            exists|j: int| #![auto] 0 <= j < i && result == lists[j].len(),
        // invariants-end
    {
        if lists[i].len() < result {
            result = lists[i].len();
        }
        i = i + 1;
    }
    result
    // impl-end
}

fn main() {}
}
