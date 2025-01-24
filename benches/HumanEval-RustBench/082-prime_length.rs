use vstd::prelude::*;

verus! {

spec fn is_divisible(n: int, divisor: int) -> (ret:bool) {
    (n % divisor) == 0
}
// pure-end

spec fn is_prime(n: int) -> (ret:bool) {
    if n < 2 {
        false
    } else {
        (forall|k: int| 2 <= k < n ==> !is_divisible(n as int, k))
    }
}
// pure-end

fn prime_length(str: &[char]) -> (result: bool)
    // post-conditions-start
    ensures
        result == is_prime(str.len() as int),
    // post-conditions-end
{
    // impl-start
    if str.len() < 2 {
        return false;
    }
    for index in 2..str.len()
        // invariants-start
        invariant
            2 <= index <= str.len(),
            forall|k: int| 2 <= k < index ==> !is_divisible(str.len() as int, k),
        // invariants-end
    {
        if ((str.len() % index) == 0) {
            assert(is_divisible(str.len() as int, index as int)); // assert-line
            return false;
        }
    }
    true
    // impl-end
}

} // verus!
fn main() {}
