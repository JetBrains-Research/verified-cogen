use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn unique_better(a: &[i32]) -> (result: Vec<i32>)
    requires
        forall|i: int, j: int|
            #![trigger a[i], a[j]]
            0 <= i && i < j && j < a.len() ==> a[i] <= a[j],
    ensures
        forall|i: int, j: int|
            #![trigger result[i], result[j]]
            0 <= i && i < j && j < result.len() ==> result[i] < result[j],
{
    let mut result: Vec<i32> = Vec::new();
    let mut i = 0;
    while i < a.len()
        invariant
            0 <= i <= a.len(),
            forall|k: int, l: int|
                #![trigger result[k], result[l]]
                0 <= k && k < l && l < result.len() ==> result[k] < result[l],
            forall|k: int|
                #![trigger result[k]]
                0 <= k && k < result.len() ==> exists|m: int| 0 <= m < i && result[k] == a[m],
    {
        if result.len() == 0 || result[result.len() - 1] != a[i] {
            assert(result.len() == 0 || result[result.len() - 1] < a[i as int]);
            result.push(a[i]);
        }
        i = i + 1;
    }
    result
}

fn main() {}
}
