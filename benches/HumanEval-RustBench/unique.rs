use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn unique(a: &[i32]) -> (result: Vec<i32>)
    // pre-conditions-start
    requires
        forall|i: int, j: int|
            #![trigger a[i], a[j]]
            0 <= i && i < j && j < a.len() ==> a[i] <= a[j],
    // pre-conditions-end
    // post-conditions-start
    ensures
        forall|i: int, j: int|
            #![trigger result[i], result[j]]
            0 <= i && i < j && j < result.len() ==> result[i] < result[j],
    // post-conditions-end
{
    // impl-start
    let mut result: Vec<i32> = Vec::new();
    let mut i = 0;
    while i < a.len()
        // invariants-start
        invariant
            0 <= i && i <= a.len(),
            forall|i: int, j: int| 0 <= i && i < j && j < a.len() ==> a[i] <= a[j],
            forall|i: int, j: int| 0 <= i && i < j && j < result.len() ==> #[trigger] result[i] < #[trigger] result[j],
            result.len() == 0 || i == a.len() || result[result.len() - 1] <= a[i as int]
        // invariants-end
    {
        if result.len() == 0 || result[result.len() - 1] != a[i] {
            assert(result.len() == 0 || result[result.len() - 1] < a[i as int]); // assert-line
            result.push(a[i]);
        }
        i = i + 1;
    }
    result
    // impl-end
}

fn main() {}
}
