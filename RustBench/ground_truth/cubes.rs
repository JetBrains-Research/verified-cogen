use vstd::prelude::*;

verus! {

#[verifier::external_body]
fn add(a: i32, b: i32) -> (result: i32)
    ensures
        result == a + b,
{
    a + b
}

#[verifier::loop_isolation(false)]
fn cubes(len: usize) -> (result: Vec<i32>) by (nonlinear_arith)
    ensures
        result.len() == len,
        forall|i: int| 0 <= i && i < len ==> result[i] == i * i * i
{
    let mut result: Vec<i32> = Vec::new();

    let mut c = 0;
    let mut k = 1;
    let mut m = 6;

    let mut n = 0;
    while n < len
        invariant
            0 <= n && n <= len,
            result.len() == n,
            forall|i: int| 0 <= i && i < n ==> result[i] == i * i * i,
            c == n * n * n,
            k == 3 * n * n + 3 * n + 1,
            m == 6 * n + 6,
    {
        result.push(c);

        c = add(c, k);
        k = add(k, m);
        m = add(m, 6);
        n = n + 1;
    }
    result
}

fn main() {}
}