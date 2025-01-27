use vstd::prelude::*;

verus! {
spec fn count<T>(s: Seq<T>, x: T) -> (result:int)
    decreases s.len(),
{
    if s.len() == 0 {
        0
    } else {
        count(s.skip(1), x) + if s[0] == x {
            1int
        } else {
            0int
        }
    }
}
// pure-end

spec fn permutes<T>(s1: Seq<T>, s2: Seq<T>) -> (result:bool) {
    forall|x: T| count(s1, x) == count(s2, x)
}
// pure-end

spec fn inner_expr_lemma_update_effect_on_count<T>(s: Seq<T>, i: int, v: T, x: T) -> (result:bool) {
    count(s.update(i, v), x) == if v == x && s[i] != x {
        count(s, x) + 1
    } else if v != x && s[i] == x {
        count(s, x) - 1
    } else {
        count(s, x)
    }
}
// pure-end

proof fn lemma_update_effect_on_count<T>(s: Seq<T>, i: int, v: T, x: T)
    // pre-conditions-start
    requires
        0 <= i < s.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        inner_expr_lemma_update_effect_on_count(s, i, v, x),
    decreases s.len(),
    // post-conditions-end
{
    // impl-start
    if s.len() == 0 {
        return ;
    }
    if i == 0 {
        assert(s.update(i, v) =~= seq![v] + s.skip(1));
        assert(s.update(i, v).skip(1) =~= s.skip(1));
    } else {
        assert(s.update(i, v) =~= seq![s[0]] + s.skip(1).update(i - 1, v));
        assert(s.update(i, v).skip(1) =~= s.skip(1).update(i - 1, v));
        lemma_update_effect_on_count(s.skip(1), i - 1, v, x);
    }
    // impl-end
}
// pure-end

proof fn lemma_swapping_produces_a_permutation<T>(s: Seq<T>, i: int, j: int)
    // pre-conditions-start
    requires
        0 <= i < s.len(),
        0 <= j < s.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        permutes(s.update(i, s[j]).update(j, s[i]), s),
    // post-conditions-end
{
    // impl-start
    assert forall|x: T| #[trigger] count(s.update(i, s[j]).update(j, s[i]), x) == count(s, x) by {
        lemma_update_effect_on_count(s, i, s[j], x);
        lemma_update_effect_on_count(s.update(i, s[j]), j, s[i], x);
    }
    // impl-end
}
// pure-end

#[verifier::loop_isolation(false)]
fn sort_pred(l: Vec<i32>, p: Vec<bool>) -> (l_prime: Vec<i32>)
    // pre-conditions-start
    requires
        l.len() == p.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        l_prime.len() == l.len(),
        forall|i: int| 0 <= i < l.len() && !p[i] ==> l_prime[i] == l[i],
        forall|i: int, j: int|
            #![auto]
            0 <= i < j < l.len() && p[i] && p[j] ==> l_prime[i] <= l_prime[j],
        permutes(l_prime@, l@),
    // post-conditions-end
{
    // impl-start
    let ghost old_l = l@;
    let l_len = l.len();
    let mut pos_replace: usize = 0;
    let mut l_prime: Vec<i32> = l;
    while pos_replace < l_len
        // invariants-start
        invariant
            l_len == l.len() == l_prime.len(),
            forall|i: int| 0 <= i < l_len && !p[i] ==> l_prime[i] == l[i],
            permutes(l_prime@, l@),
            forall|i: int, j: int|
                #![auto]
                0 <= i < pos_replace && i < j < l_len && p[i] && p[j] ==> l_prime[i] <= l_prime[j],
        // invariants-end
    {
        if p[pos_replace] {
            let mut pos_cur: usize = pos_replace;
            let mut pos: usize = pos_replace;
            while pos < l_len
                // invariants-start
                invariant
                    l_len == l.len() == l_prime.len(),
                    pos_replace <= pos,
                    pos_replace <= pos_cur < l_len,
                    p[pos_replace as int],
                    p[pos_cur as int],
                    forall|i: int| 0 <= i < l_len && !p[i] ==> l_prime[i] == l[i],
                    permutes(l_prime@, l@),
                    forall|i: int|
                        #![auto]
                        pos_replace <= i < pos && p[i] ==> l_prime[pos_cur as int] <= l_prime[i],
                    forall|i: int, j: int|
                        #![auto]
                        0 <= i < pos_replace && i < j < l_len && p[i] && p[j] ==> l_prime[i]
                            <= l_prime[j],
                // invariants-end
            {
                if p[pos] && l_prime[pos] < l_prime[pos_cur] {
                    pos_cur = pos;
                }
                pos = pos + 1;
            }
            // assert-start
            proof {
                lemma_swapping_produces_a_permutation(l_prime@, pos_replace as int, pos_cur as int);
            }
            // assert-end
            let v1 = l_prime[pos_replace];
            let v2 = l_prime[pos_cur];
            l_prime.set(pos_replace, v2);
            l_prime.set(pos_cur, v1);
        }
        pos_replace = pos_replace + 1;
    }
    l_prime
    // impl-end
}

#[verifier::loop_isolation(false)]
fn sort_even(l: Vec<i32>) -> (result: Vec<i32>)
    // post-conditions-start
    ensures
        l.len() == result.len(),
        permutes(result@, l@),
        forall|i: int| 0 <= i < l.len() && i % 2 == 1 ==> result[i] == l[i],
        forall|i: int, j: int|
            #![auto]
            0 <= i < j < l.len() && i % 2 == 0 && j % 2 == 0 ==> result[i] <= result[j],
    // post-conditions-end
{
    // impl-start
    let mut p: Vec<bool> = vec![];
    for i in 0..l.len()
        // invariants-start
        invariant
            p.len() == i,
            forall|j: int| 0 <= j < i ==> p[j] == (j % 2 == 0),
        // invariants-end
    {
        p.push(i % 2 == 0);
    }
    // assert-start
    assert(forall|i: int, j: int|
        #![auto]
        0 <= i < j < l.len() && i % 2 == 0 && j % 2 == 0 ==> p[i] && p[j]);
    // assert-end
    sort_pred(l, p)
    // impl-end
}

}
fn main() {}
