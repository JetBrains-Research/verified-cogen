use vstd::arithmetic::div_mod::{
    lemma_fundamental_div_mod, lemma_fundamental_div_mod_converse_div,
};
use vstd::prelude::*;

verus! {

spec fn mul(a: nat, b: nat) -> (result:nat) {
    builtin::mul(a, b)
}
// pure-end

spec fn divides(factor: nat, candidate: nat) -> (result:bool) {
    exists|k: nat| mul(factor, k) == candidate
}
// pure-end

proof fn lemma_mod_zero(a: nat, b: nat)
    // pre-conditions-start
    requires
        a > 0 && b > 0,
        a % b == 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        divides(b, a),
    // post-conditions-end
{
    // impl-start
    lemma_fundamental_div_mod(a as int, b as int);
    assert(mul(b, (a / b)) == a);
    // impl-end
}
// pure-end

proof fn lemma_mod_zero_reversed(a: nat, b: nat)
    // pre-conditions-start
    requires
        a > 0 && b > 0,
        divides(b, a),
    // pre-conditions-end
    // post-conditions-start
    ensures
        a % b == 0,
    // post-conditions-end
{
    // impl-start
    let k_wit = choose|k: nat| mul(b, k) == a;
    assert(k_wit == a / b) by {
        lemma_fundamental_div_mod_converse_div(a as int, b as int, k_wit as int, 0 as int);
    }
    lemma_fundamental_div_mod(a as int, b as int);
    // impl-end
}
// pure-end

proof fn lemma_one_divides_all()
    // post-conditions-start
    ensures
        forall|v: nat| divides(1 as nat, v),
    // post-conditions-end
{
    // impl-start
    assert forall|v: nat| divides(1 as nat, v) by {
        assert(mul(1 as nat, v) == v);
    }
    // impl-end
}
// pure-end

fn largest_divisor(n: u32) -> (ret: u32)
    // pre-conditions-start
    requires
        n > 1,
    // pre-conditions-end
    // post-conditions-start
    ensures
        divides(ret as nat, n as nat),
        ret < n,
        forall|k: u32| (0 < k < n && divides(k as nat, n as nat)) ==> ret >= k,
    // post-conditions-end
{
    // impl-start
    let mut i = n - 1;
    while i >= 2
        // invariants-start
        invariant
            n > 0,
            i < n,
            forall|k: u32| i < k < n ==> !divides(k as nat, n as nat),
        // invariants-end
    {
        if n % i == 0 {
            // assert-start
            assert(divides(i as nat, n as nat)) by {
                lemma_mod_zero(n as nat, i as nat);
            }
            // assert-end
            return i;
        }
        i -= 1;

        // assert-start
        assert forall|k: u32| i < k < n implies !divides(k as nat, n as nat) by {
            if k == i + 1 {
                assert(!divides(k as nat, n as nat)) by {
                    if (divides(k as nat, n as nat)) {
                        lemma_mod_zero_reversed(n as nat, k as nat);
                    }
                }
            }
        }
        // assert-end
    }
    // assert-start
    assert(divides(1 as nat, n as nat)) by {
        lemma_one_divides_all();
    }
    // assert-end
    1
    // impl-end
}

}
fn main() {}
