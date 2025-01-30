use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn is_prime(n: u32) -> (result: bool)
    // pre-conditions-start
    requires
        n >= 2,
    // pre-conditions-end
    // post-conditions-start
    ensures
        result ==> (forall|k: int| 2 <= k < n ==> #[trigger] (n as int % k) != 0),
        !result ==> exists|k: int| 2 <= k < n && #[trigger] (n as int % k) == 0,
    // post-conditions-end
{
    // impl-start
    let mut i = 2;
    let mut result = true;
    while i < n
        // invariants-start
        invariant
            2 <= i <= n,
            result ==> forall|k: int| 2 <= k < i ==> #[trigger] (n as int % k) != 0,
            !result ==> exists|k: int| 2 <= k < i && #[trigger] (n as int % k) == 0,
        // invariants-end
    {
        if n % i == 0 {
            result = false;
        }
        i = i + 1;
    }
    result
    // impl-end
}

spec fn is_prime_pred(n: u32) -> (ret: bool) {
    forall|k: int| 2 <= k < n ==> #[trigger] (n as int % k) != 0
}

#[verifier::loop_isolation(false)]
fn largest_prime_factor(n: u32) -> (result: u32)
    requires
        2 <= n <= u32::MAX - 1,
    ensures
        1 <= result <= n,
        result == 1 || (result > 1 && is_prime_pred(result))
{
    let mut largest = 1;
    let mut i = 2;
    while i <= n
        invariant
            2 <= i <= n + 1,
            1 <= largest < i,
            largest == 1 || (largest > 1 && is_prime_pred(largest)),
    {
        if n % i == 0 && is_prime(i) {
            largest = i;
        }
        i = i + 1;
    }
    largest
}

fn main() {}
}
