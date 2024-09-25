use vstd::prelude::*;

verus! {

fn max_element(a: &Vec<i32>) -> (max: i32)
    // pre-conditions-start
    requires
        a.len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        forall|i: int| 0 <= i < a.len() ==> a[i] <= max,
        exists|i: int| 0 <= i < a.len() && a[i] == max,
    // post-conditions-end
{
    // impl-start
    let mut max = a[0];
    for i in 1..a.len()
        // invariants-start
        invariant
            forall|j: int| 0 <= j < i ==> a[j] <= max,
            exists|j: int| 0 <= j < i && a[j] == max,
        // invariants-end
    {
        if a[i] > max {
            max = a[i];
        }
    }
    max
    // impl-end
}

}
fn main() {}
