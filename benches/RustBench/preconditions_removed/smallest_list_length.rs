use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn smallest_list_length(lists: Vec<Vec<i32>>) -> (result: usize)
    ensures
        exists|i: int| #![auto] 0 <= i < lists.len() && result == lists[i].len(),
        forall|i: int| #![auto] 0 <= i < lists.len() ==> result <= lists[i].len(),
{
    let mut result = lists[0].len();
    let mut i = 1;
    while i < lists.len()
        invariant
            0 <= i <= lists.len(),
            forall|j: int| #![auto] 0 <= j < i ==> result <= lists[j].len(),
            exists|j: int| #![auto] 0 <= j < i && result == lists[j].len(),
    {
        if lists[i].len() < result {
            result = lists[i].len();
        }
        i = i + 1;
    }
    result
}

fn main() {}
}
