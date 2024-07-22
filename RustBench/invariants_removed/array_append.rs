use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn array_append(a: Vec<i32>, b: i32) -> (result: Vec<i32>)
    ensures
        result.len() == a.len() + 1,
        forall|i: int| #![auto] 0 <= i && i < result.len() ==> result[i] == (if i < a.len() { a[i] } else { b }),
{
    let mut result: Vec<i32> = Vec::new();
    let mut i = 0;
    while i < a.len()
    {
        result.push(a[i]);
        i = i + 1;
    }
    result.push(b);
    result
}

fn main() {}
}
