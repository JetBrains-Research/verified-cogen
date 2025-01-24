use vstd::arithmetic::mul::*;
use vstd::prelude::*;

verus! {

spec fn spec_prime(p: int) -> (ret:bool) {
    p > 1 && forall|k: int| 1 < k < p ==> #[trigger] (p % k) != 0
}
// pure-end

fn prime(p: u32) -> (ret: bool)
    // post-conditions-start
    ensures
        ret <==> spec_prime(p as int),
    // post-conditions-end
{
    // impl-start
    if p <= 1 {
        return false;
    }
    for k in 2..p
        // invariants-start
        invariant
            forall|j: int| 1 < j < k ==> #[trigger] (p as int % j) != 0,
            k <= p,
        // invariants-end
    {
        if p % k == 0 {
            return false;
        }
    }
    true
    // impl-end
}

fn checked_mul_thrice(x: u32, y: u32, z: u32) -> (ret: Option<u32>)
    // post-conditions-start
    ensures
        ret.is_some() ==> ret.unwrap() == x * y * z,
        ret.is_none() ==> x * y * z > u32::MAX,
    // post-conditions-end
{
    // impl-start
    if (x == 0 || y == 0 || z == 0) {
        return Some(0);
    }
    assert(x > 0 && y > 0 && z > 0); // assert-line
    let prod2 = x.checked_mul(y);
    if prod2.is_some() {
        let prod3 = prod2.unwrap().checked_mul(z);
        if prod3.is_some() {
            let ans = prod3.unwrap();
            assert(ans == x * y * z); // assert-line
            Some(ans)
        } else {
            assert(x * y * z > u32::MAX); // assert-line
            None
        }
    } else {
        // assert-start
        broadcast use group_mul_properties;

        assert(x * y * z >= y * z);
        // assert-end
        None
    }
    // impl-end
}

fn is_multiply_prime(x: u32) -> (ans: bool)
    // pre-conditions-start
    requires
        x > 1,
    // pre-conditions-end
    // post-conditions-start
    ensures
        ans <==> exists|a: int, b: int, c: int|
            spec_prime(a) && spec_prime(b) && spec_prime(c) && x == a * b * c,
    // post-conditions-end
{
    // impl-start
    let mut a = 1;
    while a < x
        // invariants-start
        invariant
            forall|i: int, j: int, k: int|
                (spec_prime(i) && spec_prime(j) && spec_prime(k) && i <= a && j <= x && k <= x)
                    ==> x != i * j * k,
            a <= x,
        // invariants-end
    {
        a += 1;
        if prime(a) {
            let mut b = 1;
            while b < x
                // invariants-start
                invariant
                    forall|j: int, k: int|
                        (spec_prime(j) && spec_prime(k) && j <= b && k <= x) ==> x != (a as int) * j
                            * k,
                    spec_prime(a as int),
                    a <= x,
                    b <= x,
                // invariants-end
            {
                b += 1;
                if prime(b) {
                    let mut c = 1;
                    while c < x
                        // invariants-start
                        invariant
                            forall|k: int| (spec_prime(k) && k <= c as int) ==> x != a * b * k,
                            spec_prime(a as int),
                            spec_prime(b as int),
                            a <= x,
                            b <= x,
                            c <= x,
                        // invariants-end
                    {
                        c += 1;
                        let prod = checked_mul_thrice(a, b, c);
                        if prime(c) && prod.is_some() && x == prod.unwrap() {
                            return true;
                        }
                    }
                }
            }
        }
    }
    // assert-start
    assert(forall|i: int, j: int, k: int|
        i <= x && j <= x && k <= x && spec_prime(i) && spec_prime(j) && spec_prime(k) ==> x != i * j
            * k);
    // assert-end
    // assert-start
    assert forall|i: int, j: int, k: int|
        spec_prime(i) && spec_prime(j) && spec_prime(k) ==> x != i * j * k by {
        if (i > 1 && j > 1 && k > 1 && (i > x || j > x || k > x)) {
            broadcast use group_mul_properties;
            assert(i * j * k > x);
        }
    }
    // assert-end
    false
    // impl-end
}

}
fn main() {}
