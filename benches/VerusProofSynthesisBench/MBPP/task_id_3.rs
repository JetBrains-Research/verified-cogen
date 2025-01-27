use vstd::prelude::*;


verus! {

spec fn is_divisible(n: int, divisor: int) -> bool {
    (n % divisor) == 0
}
// pure-end

fn is_non_prime(n: u64) -> (result: bool)
    // pre-conditions-start
    requires
        n >= 2,
    // pre-conditions-end
    // post-conditions-start
    ensures
        result == (exists|k: int| 2 <= k < n && is_divisible(n as int, k)),
    // post-conditions-end
{
    // impl-start
    if n <= 1 {
        return true;
    }
    let mut index = 2;
    while index < n
        // invariants-start
        invariant
            2 <= index,
            forall|k: int| 2 <= k < index ==> !is_divisible(n as int, k),
        // invariants-end
    {
        if ((n % index) == 0) {
            // assert-start
            assert(is_divisible(n as int, index as int));
            // assert-end
            return true;
        }
        index += 1;
    }
    false
    // impl-end
}

} // verus!

fn main() {}
