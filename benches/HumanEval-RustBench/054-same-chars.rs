use vstd::hash_set::HashSetWithView;
use vstd::prelude::*;
use vstd::std_specs::hash::axiom_u8_obeys_hash_table_key_model;

verus! {

broadcast use axiom_u8_obeys_hash_table_key_model;

fn hash_set_from(s: &Vec<u8>) -> (res: HashSetWithView<u8>)
    // post-conditions-start
    ensures
        forall|i: int| #![auto] 0 <= i < s.len() ==> res@.contains(s[i]),
        forall|x: int|
            0 <= x < 256 ==> #[trigger] res@.contains(x as u8) ==> #[trigger] s@.contains(x as u8),
    // post-conditions-end
{
    // impl-start
    let mut res: HashSetWithView<u8> = HashSetWithView::new();
    for i in 0..s.len()
        // invariants-start
        invariant
            forall|j: int| #![auto] 0 <= j < i ==> res@.contains(s[j]),
            forall|x: int|
                0 <= x < 256 ==> #[trigger] res@.contains(x as u8) ==> (exists|j: int|
                    0 <= j < i && s[j] == x),
        // invariants-end
    {
        res.insert(s[i]);
    }
    res
    // impl-end
}

proof fn implies_contains(s0: Seq<u8>, s1: Seq<u8>, hs1: Set<u8>)
    // pre-conditions-start
    requires
        forall|i: int| #![trigger s0[i]] 0 <= i < s0.len() ==> 0 <= s0[i] < 256,
        forall|x: int|
            0 <= x < 256 ==> #[trigger] hs1.contains(x as u8) ==> #[trigger] s1.contains(x as u8),
    // pre-conditions-end
    // post-conditions-start
    ensures
        forall|i: int|
            #![auto]
            0 <= i < s0.len() && 0 <= s0[i] < 256 && hs1.contains(s0[i]) ==> s1.contains(s0[i]),
    // post-conditions-end
{
    // impl-start
    assert forall|i: int|
        #![auto]
        0 <= i < s0.len() && 0 <= s0[i] < 256 && hs1.contains(s0[i]) implies s1.contains(s0[i]) by {
        let x = s0[i];
        assert(0 <= x < 256);
        assert(hs1.contains(x as u8));
        assert(s1.contains(x as u8));
    };
    // impl-end
}
// pure-end

#[verifier::loop_isolation(false)]
fn same_chars(s0: &Vec<u8>, s1: &Vec<u8>) -> (same: bool)
    // post-conditions-start
    ensures
        same <==> (forall|i: int| #![auto] 0 <= i < s0.len() ==> s1@.contains(s0[i])) && (forall|
            i: int,
        |
            #![auto]
            0 <= i < s1.len() ==> s0@.contains(s1[i])),
    // post-conditions-end
{
    // impl-start
    let hs0 = hash_set_from(s0);
    let hs1 = hash_set_from(s1);

    // assert-start
    proof {
        implies_contains(s0@, s1@, hs1@);
        implies_contains(s1@, s0@, hs0@);
    }
    // assert-end

    let mut contains_s0 = true;
    for i in 0..s0.len()
        // invariants-start
        invariant
            contains_s0 <==> forall|j: int| #![auto] 0 <= j < i ==> s1@.contains(s0[j]),
        // invariants-end
    {
        if !hs1.contains(&s0[i]) {
            contains_s0 = false;
            assert(!s1@.contains(s0[i as int])); // assert-line
        }
    }
    let mut contains_s1 = true;
    for i in 0..s1.len()
        // invariants-start
        invariant
            contains_s1 <==> forall|j: int| #![auto] 0 <= j < i ==> s0@.contains(s1[j]),
        // invariants-end
    {
        if !hs0.contains(&s1[i]) {
            contains_s1 = false;
            assert(!s0@.contains(s1[i as int])); // assert-line
        }
    }
    contains_s0 && contains_s1
    // impl-end
}

}
fn main() {}
