use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn array_copy(a: Vec<i32>) -> (result: Vec<i32>)
    ensures
        result.len() == a.len(),
        forall|i: int| 0 <= i && i < a.len() ==> result[i] == a[i],
{
    let mut result: Vec<i32> = Vec::new();
    let mut i = 0;
    while i < a.len()
    {
        result.push(a[i]);
        i = i + 1;
    }
    result
}

fn main() {}
}
