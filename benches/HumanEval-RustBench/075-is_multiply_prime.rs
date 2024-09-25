use vstd::arithmetic::mul::*;
use vstd::prelude::*;

verus! {

spec fn spec_prime(p: int) -> bool {
    p > 1 && forall|k: int| 1 < k < p ==> #[trigger] (p % k) != 0
}

fn prime(p: u32) -> (ret: bool)
    ensures
        ret <==> spec_prime(p as int),
{
    if p <= 1 {
        return false;
    }
    for k in 2..p
        invariant
            forall|j: int| 1 < j < k ==> #[trigger] (p as int % j) != 0,
            k <= p,
    {
        if p % k == 0 {
            return false;
        }
    }
    true
}

fn checked_mul_thrice(x: u32, y: u32, z: u32) -> (ret: Option<u32>)
    ensures
        ret.is_some() ==> ret.unwrap() == x * y * z,
        ret.is_none() ==> x * y * z > u32::MAX,
{
    if (x == 0 || y == 0 || z == 0) {
        return Some(0);
    }
    assert(x > 0 && y > 0 && z > 0);
    let prod2 = x.checked_mul(y);
    if prod2.is_some() {
        let prod3 = prod2.unwrap().checked_mul(z);
        if prod3.is_some() {
            let ans = prod3.unwrap();
            assert(ans == x * y * z);
            Some(ans)
        } else {
            assert(x * y * z > u32::MAX);
            None
        }
    } else {
        broadcast use group_mul_properties;

        assert(x * y * z >= y * z);
        None
    }
}

fn is_multiply_prime(x: u32) -> (ans: bool)
    requires
        x > 1,
    ensures
        ans <==> exists|a: int, b: int, c: int|
            spec_prime(a) && spec_prime(b) && spec_prime(c) && x == a * b * c,
{
    let mut a = 1;
    while a < x
        invariant
            forall|i: int, j: int, k: int|
                (spec_prime(i) && spec_prime(j) && spec_prime(k) && i <= a && j <= x && k <= x)
                    ==> x != i * j * k,
            a <= x,
    {
        a += 1;
        if prime(a) {
            let mut b = 1;
            while b < x
                invariant
                    forall|j: int, k: int|
                        (spec_prime(j) && spec_prime(k) && j <= b && k <= x) ==> x != (a as int) * j
                            * k,
                    spec_prime(a as int),
                    a <= x,
                    b <= x,
            {
                b += 1;
                if prime(b) {
                    let mut c = 1;
                    while c < x
                        invariant
                            forall|k: int| (spec_prime(k) && k <= c as int) ==> x != a * b * k,
                            spec_prime(a as int),
                            spec_prime(b as int),
                            a <= x,
                            b <= x,
                            c <= x,
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
    assert(forall|i: int, j: int, k: int|
        i <= x && j <= x && k <= x && spec_prime(i) && spec_prime(j) && spec_prime(k) ==> x != i * j
            * k);
    assert forall|i: int, j: int, k: int|
        spec_prime(i) && spec_prime(j) && spec_prime(k) ==> x != i * j * k by {
        if (i > 1 && j > 1 && k > 1 && (i > x || j > x || k > x)) {
            broadcast use group_mul_properties;

            assert(i * j * k > x);
        }
    }
    false
}

} 
fn main() {}
