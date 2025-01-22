
use vstd::prelude::*;

verus! {

spec fn sum(s: Seq<int>) -> (result:int)
    decreases s.len(),
{
    if s.len() == 0 {
        0
    } else {
        s[0] + sum(s.skip(1))
    }
}
// pure-end

spec fn sum_other_way(s: Seq<int>) -> (result:int)
    decreases s.len(),
{
    if s.len() == 0 {
        0
    } else {
        s[s.len() - 1] + sum_other_way(s.take(s.len() - 1))
    }
}
// pure-end

proof fn lemma_sum_equals_sum_other_way(s: Seq<int>)
    // post-conditions-start
    ensures
        sum(s) == sum_other_way(s),
    decreases s.len(),
    // post-conditions-end
{
    // impl-start
    if s.len() == 1 {
        assert(sum(s.skip(1)) == 0);
        assert(sum_other_way(s.take(s.len() - 1)) == 0);
    } else if s.len() > 1 {
        let ss = s.skip(1);
        lemma_sum_equals_sum_other_way(ss);
        assert(sum_other_way(ss) == ss[ss.len() - 1] + sum_other_way(ss.take(ss.len() - 1)));
        lemma_sum_equals_sum_other_way(ss.take(ss.len() - 1));
        assert(ss.take(ss.len() - 1) == s.take(s.len() - 1).skip(1));
        lemma_sum_equals_sum_other_way(s.take(s.len() - 1));
    }
    // impl-end
}
// pure-end

fn below_zero(operations: Vec<i32>) -> (result: bool)
    // pre-conditions-start
    requires
        forall|i: int|
            0 <= i <= operations@.len() ==> sum(operations@.take(i).map(|_idx, j: i32| j as int))
                <= i32::MAX,
    // pre-conditions-end
    // post-conditions-start
    ensures
        result <==> exists|i: int|
            0 <= i <= operations@.len() && sum(operations@.take(i).map(|_idx, j: i32| j as int))
                < 0,
    // post-conditions-end
{
    // impl-start
    let mut s = 0i32;
    for k in 0..operations.len()
        // invariants-start
        invariant
            s == sum(operations@.take(k as int).map(|_idx, j: i32| j as int)),
            forall|i: int|
                0 <= i <= operations@.len() ==> sum(
                    operations@.take(i).map(|_idx, j: i32| j as int),
                ) <= i32::MAX,
            forall|i: int|
                0 <= i <= k ==> sum(operations@.take(i).map(|_idx, j: i32| j as int)) >= 0,
        // invariants-end
    {
        // assert-start
        assert(s + operations@[k as int] == sum(
            operations@.take(k + 1).map(|_idx, j: i32| j as int),
        )) by {
            let q1 = operations@.take(k as int).map(|_idx, j: i32| j as int);
            let q2 = operations@.take(k + 1).map(|_idx, j: i32| j as int);
            assert(q2[q2.len() - 1] == operations@[k as int] as int);
            assert(q2.take(q2.len() - 1) == q1);
            lemma_sum_equals_sum_other_way(q1);
            lemma_sum_equals_sum_other_way(q2);
        }
        // assert-end
        s = s + operations[k];
        if s < 0 {
            return true;
        }
    }
    false
    // impl-end
}

}
fn main() {}
