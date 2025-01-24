use vstd::prelude::*;

verus! {

#[verifier::external_body]
fn add_one(n: i32) -> (result: i32)
    ensures
        result == n + 1,
{
    n + 1
}

#[verifier::external_body]
fn square(n: i32) -> (result: i32)
    ensures
        n * n == result,
{
    n * n
}

fn integer_square_root(n: i32) -> (result: i32)
    // pre-conditions-start
    requires
        n >= 1,
    // pre-conditions-end
    // post-conditions-start
    ensures
        0 <= result * result,
        result * result <= n,
        n < (result + 1) * (result + 1)
    // post-conditions-end
{
    // impl-start
    let mut result = 0;
    while square(add_one(result)) <= n
        // invariants-start
        invariant
            0 <= result,
            0 <= result * result <= n
        // invariants-end
    {
        result = add_one(result);
    }
    result
    // impl-end
}

fn main() {}
}
