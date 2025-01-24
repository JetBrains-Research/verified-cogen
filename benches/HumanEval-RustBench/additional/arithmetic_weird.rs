use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn arithmetic_weird() -> (result: i32)
    // post-conditions-start
    ensures
        result < 10
    // post-conditions-end
{
    // impl-start
    let mut x = 0;
    let mut y = 0;
    while x <= 10
        // invariants-start
        invariant
            (x == 0 && y == 0) || y == 10 - x + 1
        // invariants-end
    {
        y = 10 - x;
        x = x + 1;
    }
    y
    // impl-end
}

fn main() {}
}
