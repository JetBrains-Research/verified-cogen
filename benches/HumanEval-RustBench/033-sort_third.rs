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

proof fn lemma_update_effect_on_count<T>(s: Seq<T>, i: int, v: T, x: T)
    // pre-conditions-start
    requires
        0 <= i < s.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        count(s.update(i, v), x) == if v == x && s[i] != x {
            count(s, x) + 1
        } else if v != x && s[i] == x {
            count(s, x) - 1
        } else {
            count(s, x)
        },
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

fn sort_third(l: Vec<i32>) -> (l_prime: Vec<i32>)
    // post-conditions-start
    ensures
        l_prime.len() == l.len(),
        forall|i: int| 0 <= i < l.len() && i % 3 != 0 ==> l_prime[i] == l[i],
        forall|i: int, j: int|
            0 <= i < j < l.len() && i % 3 == 0 && j % 3 == 0 ==> l_prime[i] <= l_prime[j],
        permutes(l_prime@, l@),
    // post-conditions-end
{
    // impl-start
    let ghost old_l = l@;
    let l_len = l.len();
    let mut pos_being_set_to_smallest: usize = 0;
    let mut l_prime: Vec<i32> = l;
    while pos_being_set_to_smallest < l_len
        // invariants-start
        invariant
            l_len == l.len() == l_prime.len(),
            pos_being_set_to_smallest % 3 == 0,
            forall|i: int| 0 <= i < l_len && i % 3 != 0 ==> l_prime[i] == l[i],
            permutes(l_prime@, l@),
            forall|i: int, j: int|
                0 <= i < pos_being_set_to_smallest && i < j < l_len && i % 3 == 0 && j % 3 == 0
                    ==> l_prime[i] <= l_prime[j],
        // invariants-end
    {
        let mut pos_of_smallest_found_so_far: usize = pos_being_set_to_smallest;
        let mut pos_during_scan_for_smallest: usize = pos_being_set_to_smallest;
        while pos_during_scan_for_smallest < l_len
            // invariants-start
            invariant
                l_len == l.len() == l_prime.len(),
                pos_being_set_to_smallest % 3 == 0,
                pos_during_scan_for_smallest % 3 == 0,
                pos_of_smallest_found_so_far % 3 == 0,
                pos_being_set_to_smallest <= pos_during_scan_for_smallest,
                pos_being_set_to_smallest <= pos_of_smallest_found_so_far < l_len,
                forall|i: int| 0 <= i < l_len && i % 3 != 0 ==> l_prime[i] == l[i],
                permutes(l_prime@, l@),
                forall|i: int|
                    pos_being_set_to_smallest <= i < pos_during_scan_for_smallest && i % 3 == 0
                        ==> l_prime[pos_of_smallest_found_so_far as int] <= l_prime[i],
                forall|i: int, j: int|
                    0 <= i < pos_being_set_to_smallest && i < j < l_len && i % 3 == 0 && j % 3 == 0
                        ==> l_prime[i] <= l_prime[j],
            // invariants-end
        {
            if l_prime[pos_during_scan_for_smallest] < l_prime[pos_of_smallest_found_so_far] {
                pos_of_smallest_found_so_far = pos_during_scan_for_smallest;
            }
            pos_during_scan_for_smallest = pos_during_scan_for_smallest + 3;
        }
        // assert-start
        proof {
            lemma_swapping_produces_a_permutation(
                l_prime@,
                pos_being_set_to_smallest as int,
                pos_of_smallest_found_so_far as int,
            );
        }
        // assert-end
        let v1 = l_prime[pos_being_set_to_smallest];
        let v2 = l_prime[pos_of_smallest_found_so_far];
        l_prime.set(pos_being_set_to_smallest, v2);
        l_prime.set(pos_of_smallest_found_so_far, v1);
        pos_being_set_to_smallest = pos_being_set_to_smallest + 3;
    }
    l_prime
    // impl-end
}

}
fn main() {}
