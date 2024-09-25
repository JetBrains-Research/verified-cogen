use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn is_non_prime(n: u32) -> (result: bool)
    // pre-conditions-start
    requires
        n >= 2,
    // pre-conditions-end
    // post-conditions-start
    ensures
        result == exists|k: int| 2 <= k < n && #[trigger] (n as int % k) == 0,
    // post-conditions-end
{
    // impl-start
    let mut i = 2;
    while i < n
        // invariants-start
        invariant
            2 <= i <= n,
            forall|k: int| 2 <= k < i ==> #[trigger] (n as int % k) != 0,
        // invariants-end
    {
        if n % i == 0 {
            return true;
        }
        i = i + 1;
    }
    false
    // impl-end
}

fn main() {}
}
