use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn unique(a: &[i32]) -> (result: Vec<i32>)
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