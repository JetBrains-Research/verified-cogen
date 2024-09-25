use vstd::arithmetic::div_mod::{
    lemma_fundamental_div_mod, lemma_fundamental_div_mod_converse_div,
};
use vstd::prelude::*;

verus! {

pub open spec fn mul(a: nat, b: nat) -> nat {
    builtin::mul(a, b)
}
pub open spec fn divides(factor: nat, candidate: nat) -> bool {
    exists|k: nat| mul(factor, k) == candidate
}
proof fn lemma_mod_zero(a: nat, b: nat)
    requires
        a > 0 && b > 0,
        a % b == 0,
    ensures
        divides(b, a),
{
    lemma_fundamental_div_mod(a as int, b as int);
    assert(mul(b, (a / b)) == a);
}
proof fn lemma_mod_zero_reversed(a: nat, b: nat)
    requires
        a > 0 && b > 0,
        divides(b, a),
    ensures
        a % b == 0,
{
    let k_wit = choose|k: nat| mul(b, k) == a;
    assert(k_wit == a / b) by {
        lemma_fundamental_div_mod_converse_div(a as int, b as int, k_wit as int, 0 as int);
    }
    lemma_fundamental_div_mod(a as int, b as int);
}
proof fn lemma_one_divides_all()
    ensures
        forall|v: nat| divides(1 as nat, v),
{
    assert forall|v: nat| divides(1 as nat, v) by {
        assert(mul(1 as nat, v) == v);
    }
}
fn largest_divisor(n: u32) -> (ret: u32)
    requires
        n > 1,
    ensures
        divides(ret as nat, n as nat),
        ret < n,
        forall|k: u32| (0 < k < n && divides(k as nat, n as nat)) ==> ret >= k,
{
    let mut i = n - 1;
    while i >= 2
        invariant
            n > 0,
            i < n,
            forall|k: u32| i < k < n ==> !divides(k as nat, n as nat),
    {
        if n % i == 0 {
            assert(divides(i as nat, n as nat)) by {
                lemma_mod_zero(n as nat, i as nat);
            }
            return i;
        }
        i -= 1;

        assert forall|k: u32| i < k < n implies !divides(k as nat, n as nat) by {
            if k == i + 1 {
                assert(!divides(k as nat, n as nat)) by {
                    if (divides(k as nat, n as nat)) {
                        lemma_mod_zero_reversed(n as nat, k as nat);
                    }
                }
            }
        }
    }
    assert(divides(1 as nat, n as nat)) by {
        lemma_one_divides_all();
    }
    1
}

} 
fn main() {}
