use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn remove_element(a: &[i32], pos: usize) -> (result: Vec<i32>)
    requires
        0 <= pos < a.len(),
    ensures
        result.len() == a.len() - 1,
        forall|i: int| 0 <= i < pos ==> result[i] == a[i],
        forall|i: int| pos <= i < result.len() ==> result[i] == a[i + 1],
{
    let mut result: Vec<i32> = Vec::new();
    let mut i = 0;
    while i < pos
        invariant
            0 <= i <= pos,
            forall|k: int| 0 <= k < i ==> result[k] == a[k],
            result.len() == i,
    {
        result.push(a[i]);
        i = i + 1;
    }

    while i + 1 < a.len()
        invariant
            pos <= i < a.len(),
            result.len() == i,
            forall|k: int| 0 <= k < pos ==> result[k] == a[k],
            forall|k: int| pos <= k < i ==> result[k] == a[k + 1],
    {
        result.push(a[i + 1]);
        i = i + 1;
    }
    result
}

fn main() {}
}