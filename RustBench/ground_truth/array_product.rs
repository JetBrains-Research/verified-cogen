use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn array_product(a: Vec<i32>, b: Vec<i32>) -> (result: Vec<i64>) by (nonlinear_arith)
    requires
        a.len() == b.len(),
    ensures
        result.len() == a.len(),
        forall|i: int| #![auto] 0 <= i && i < a.len() ==> result[i] == (a[i] as i64) * (b[i] as i64),
{
    let mut result: Vec<i64> = Vec::new();
    let mut i = 0;
    while i < a.len()
        invariant
            0 <= i && i <= a.len(),
            result.len() == i,
            forall|j: int| #![auto] 0 <= j && j < i ==> result[j] == (a[j] as i64) * (b[j] as i64), 
    {
        result.push(a[i] as i64 * b[i] as i64);
        i = i + 1;
    }
    result
}

fn main() {}
}
