use vstd::prelude::*;

verus! {
spec fn spec_prime_helper(num: int, limit: int) -> (ret:bool) {
    forall|j: int| 2 <= j < limit ==> (#[trigger] (num % j)) != 0
}
// pure-end

spec fn spec_prime(num: int) -> (ret:bool) {
    spec_prime_helper(num, num)
}
// pure-end

fn is_prime(num: u32) -> (result: bool)
    // pre-conditions-start
    requires
        num >= 2,
    // pre-conditions-end
    // post-conditions-start
    ensures
        result <==> spec_prime(num as int),
    // post-conditions-end
{
    // impl-start
    let mut i = 2;
    let mut result = true;
    while i < num
        // invariants-start
        invariant
            2 <= i <= num,
            result <==> spec_prime_helper(num as int, i as int),
        // invariants-end
    {
        if num % i == 0 {
            result = false;
        }
        i += 1;
    }
    result
    // impl-end
}

fn largest_prime_factor(n: u32) -> (largest: u32)
    // pre-conditions-start
    requires
        n >= 2,
    // pre-conditions-end
    // post-conditions-start
    ensures
        1 <= largest <= n,
        spec_prime(largest as int),
    // post-conditions-end
{
    // impl-start
    let mut largest = 1;
    let mut j = 1;
    while j < n
        // invariants-start
        invariant
            1 <= largest <= j <= n,
            spec_prime(largest as int),
        // invariants-end
    {
        j += 1;
        let flag = is_prime(j);
        if n % j == 0 && flag {
            largest =
            if largest > j {
                largest
            } else {
                j
            };
        }
    }
    largest
    // impl-end
}

}
fn main() {}
