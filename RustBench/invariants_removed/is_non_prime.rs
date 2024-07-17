use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn is_non_prime(n: u32) -> (result: bool)
    requires
        n >= 2,
    ensures
        result == exists|k: int| 2 <= k < n && #[trigger] (n as int % k) == 0,
{
    let mut i = 2;
    while i < n
    {
        if n % i == 0 {
            return true;
        }
        i = i + 1;
    }
    false
}

fn main() {}
}
