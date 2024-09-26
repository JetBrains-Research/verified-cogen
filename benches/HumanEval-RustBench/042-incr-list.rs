use vstd::prelude::*;

verus! {

fn incr_list(l: Vec<i32>) -> (result: Vec<i32>)
    // pre-conditions-start
    requires
        forall|i: int| 0 <= i < l.len() ==> l[i] + 1 <= i32::MAX,
    // pre-conditions-end

    // post-conditions-start
    ensures
        result.len() == l.len(),
        forall|i: int| 0 <= i < l.len() ==> #[trigger] result[i] == l[i] + 1,
    // post-conditions-end
{
    // impl-start
    let mut result = Vec::with_capacity(l.len());
    for i in 0..l.len()
        // invariants-start
        invariant
            forall|i: int| 0 <= i < l.len() ==> l[i] + 1 <= i32::MAX,
            result.len() == i,
            forall|j: int| 0 <= j < i ==> #[trigger] result[j] == l[j] + 1,
        // invariants-end
    {
        result.push(l[i] + 1);
    }
    result
    // impl-end
}

}
fn main() {}
