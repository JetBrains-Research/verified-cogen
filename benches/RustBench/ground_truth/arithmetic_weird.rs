use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn arithmetic_weird() -> (result: i32)
    ensures
        result < 10
{
    let mut x = 0;
    let mut y = 0;
    while x <= 10
        invariant
            (x == 0 && y == 0) || y == 10 - x + 1
    {
        y = 10 - x;
        x = x + 1;
    }
    y
}

fn main() {}
}
