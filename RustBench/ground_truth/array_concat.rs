use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn array_concat(a: Vec<i32>, b: Vec<i32>) -> (result: Vec<i32>)
    ensures
        result.len() == a.len() + b.len(),
        forall|i: int| 0 <= i && i < a.len() ==> result[i] == a[i],
        forall|i: int| 0 <= i && i < b.len() ==> result[i + a.len()] == b[i],
{
    let mut result: Vec<i32> = Vec::new();
    let mut i = 0;
    while i < a.len()
        invariant
            0 <= i && i <= a.len(),
            result.len() == i,
            forall|j: int| 0 <= j && j < i ==> result[j] == a[j],
    {
        result.push(a[i]);
        i = i + 1;
    }
    let mut j = 0;
    while j < b.len()
        invariant
            0 <= i && i <= a.len(),
            0 <= j && j <= b.len(),
            result.len() == i + j,
            forall|k: int| 0 <= k && k < i ==> result[k] == a[k],
            forall|k: int| 0 <= k && k < j ==> result[k + i] == b[k],
    {
        result.push(b[j]);
        j = j + 1;
    }
    result
}

fn main() {}
}
