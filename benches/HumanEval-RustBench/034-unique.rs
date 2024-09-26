use vstd::calc;
use vstd::prelude::*;
use vstd::seq_lib::lemma_multiset_commutative;
use vstd::seq_lib::lemma_seq_contains_after_push;

verus! {

proof fn swap_preserves_multiset_helper(s: Seq<i32>, i: int, j: int)
    requires
        0 <= i < j < s.len(),
    ensures
        (s.take(j + 1)).to_multiset() =~= s.take(i).to_multiset().add(
            s.subrange(i + 1, j).to_multiset(),
        ).insert(s.index(j)).insert(s.index(i)),
{
    let fst = s.take(i);
    let snd = s.subrange(i + 1, j);

    assert((s.take(j + 1)).to_multiset() =~= fst.to_multiset().insert(s.index(i)).add(
        snd.to_multiset().insert(s.index(j)),
    )) by {
        assert(s.take(i + 1).to_multiset() =~= fst.to_multiset().insert(s.index(i))) by {
            fst.to_multiset_ensures();
            assert(fst.push(s.index(i)) =~= s.take(i + 1));
        }
        assert(s.subrange(i + 1, j + 1).to_multiset() =~= snd.to_multiset().insert(s.index(j))) by {
            snd.to_multiset_ensures();
            assert(snd.push(s.index(j)) =~= s.subrange(i + 1, j + 1));
        }
        lemma_multiset_commutative(s.take(i + 1), s.subrange(i + 1, j + 1));
        assert(s.take(i + 1) + s.subrange(i + 1, j + 1) =~= s.take(j + 1));
    }
}
proof fn swap_preserves_multiset(s1: Seq<i32>, s2: Seq<i32>, i: int, j: int)
    requires
        0 <= i < j < s1.len() == s2.len(),
        forall|x: int| 0 <= x < s1.len() && x != i && x != j ==> s1.index(x) == s2.index(x),
        s1.index(i) == s2.index(j),
        s1.index(j) == s2.index(i),
    ensures
        s1.to_multiset() == s2.to_multiset(),
{
    calc! {
        (==)
        s1.to_multiset(); {
            lemma_multiset_commutative(s1.take(j + 1), s1.skip(j + 1));
            assert(s1 =~= s1.take(j + 1) + s1.skip(j + 1));
        }
        s1.take(j + 1).to_multiset().add(s1.skip(j + 1).to_multiset()); {
            assert(s1.take(j + 1).to_multiset() =~= s2.take(j + 1).to_multiset()) by {
                assert(s1.take(i) == s2.take(i));
                assert(s1.subrange(i + 1, j) =~= (s2.subrange(i + 1, j)));
                swap_preserves_multiset_helper(s1, i, j);
                swap_preserves_multiset_helper(s2, i, j);
            }
            assert(s1.skip(j + 1).to_multiset() =~= s2.skip(j + 1).to_multiset()) by {
                assert(s1.skip(j + 1) =~= s2.skip(j + 1));
            }
        }
        s2.take(j + 1).to_multiset().add(s2.skip(j + 1).to_multiset()); {
            lemma_multiset_commutative(s2.take(j + 1), s2.skip(j + 1));
            assert(s2 =~= s2.take(j + 1) + s2.skip(j + 1));
        }
        s2.to_multiset();
    }
}

fn sort_seq(s: &Vec<i32>) -> (ret: Vec<i32>)
    ensures
        forall|i: int, j: int| 0 <= i < j < ret@.len() ==> ret@.index(i) <= ret@.index(j),
        ret@.len() == s@.len(),
        s@.to_multiset() == ret@.to_multiset(),
{
    let mut sorted = s.clone();
    let mut i: usize = 0;
    while i < sorted.len()
        invariant
            i <= sorted.len(),
            forall|j: int, k: int| 0 <= j < k < i ==> sorted@.index(j) <= sorted@.index(k),
            s@.to_multiset() == sorted@.to_multiset(),
            forall|j: int, k: int|
                0 <= j < i <= k < sorted@.len() ==> sorted@.index(j) <= sorted@.index(k),
            sorted@.len() == s@.len(),
    {
        let mut min_index: usize = i;
        let mut j: usize = i + 1;
        while j < sorted.len()
            invariant
                i <= min_index < j <= sorted.len(),
                forall|k: int| i <= k < j ==> sorted@.index(min_index as int) <= sorted@.index(k),
        {
            if sorted[j] < sorted[min_index] {
                min_index = j;
            }
            j += 1;
        }
        if min_index != i {
            let ghost old_sorted = sorted@;
            let curr_val = sorted[i];
            let min_val = sorted[min_index];
            sorted.set(i, min_val);

            sorted.set(min_index, curr_val);

            proof {
                swap_preserves_multiset(old_sorted, sorted@, i as int, min_index as int);
                assert(old_sorted.to_multiset() =~= sorted@.to_multiset());
            }
        }
        i += 1;
    }
    sorted
}

fn unique_sorted(s: Vec<i32>) -> (result: Vec<i32>)
    // pre-conditions-start
    requires
        forall|i: int, j: int| 0 <= i < j < s.len() ==> s[i] <= s[j],
    // pre-conditions-end
    // post-conditions-start
    ensures
        forall|i: int, j: int| 0 <= i < j < result.len() ==> result[i] < result[j],
        forall|i: int| #![auto] 0 <= i < result.len() ==> s@.contains(result[i]),
        forall|i: int| #![trigger s[i]] 0 <= i < s.len() ==> result@.contains(s[i]),
    // post-conditions-end
{
    // impl-start
    let mut result: Vec<i32> = vec![];
    for i in 0..s.len()
        // invariants-start
        invariant
            forall|i: int, j: int| 0 <= i < j < s.len() ==> s[i] <= s[j],
            forall|k: int, l: int| 0 <= k < l < result.len() ==> result[k] < result[l],
            forall|k: int|
                #![trigger result[k]]
                0 <= k < result.len() ==> (exists|m: int| 0 <= m < i && result[k] == s[m]),
            forall|m: int| #![trigger s[m]] 0 <= m < i ==> result@.contains(s[m]),
        // invariants-end
    {
        let ghost pre = result;
        if result.len() == 0 || result[result.len() - 1] != s[i] {
            assert(result.len() == 0 || result[result.len() - 1] < s[i as int]); // assert-line
            result.push(s[i]);
            // assert-start
            assert forall|m: int| #![trigger s[m]] 0 <= m < i implies result@.contains(s[m]) by {
                assert(pre@.contains(s@[m]));
                lemma_seq_contains_after_push(pre@, s@[i as int], s@[m]);
            };
            // assert-end
        }
        // assert-start
        assert(forall|m: int|
            #![trigger result@[m], pre@[m]]
            0 <= m < pre.len() ==> pre@.contains(result@[m]) ==> result@.contains(pre@[m])) by {
            assert(forall|m: int| 0 <= m < pre.len() ==> result@[m] == pre@[m]);
        }
        // assert-end
        // assert-start
        assert(result@.contains(s[i as int])) by {
            assert(result[result.len() - 1] == s[i as int]);
        }
        // assert-end
    }
    result
    // impl-end
}

fn unique(s: Vec<i32>) -> (result: Vec<i32>)
    // post-conditions-start
    ensures
        forall|i: int, j: int| 0 <= i < j < result.len() ==> result[i] < result[j],
        forall|i: int| #![auto] 0 <= i < result.len() ==> s@.contains(result[i]),
        forall|i: int| #![trigger s[i]] 0 <= i < s.len() ==> result@.contains(s[i]),
    // post-conditions-end
{
    // impl-start
    let sorted = sort_seq(&s);
    // assert-start
    assert(forall|i: int| #![auto] 0 <= i < sorted.len() ==> s@.contains(sorted[i])) by {
        assert(forall|i: int|
            #![auto]
            0 <= i < sorted.len() ==> sorted@.to_multiset().contains(sorted[i])) by {
            sorted@.to_multiset_ensures();
        }
        assert(forall|i: int|
            #![auto]
            0 <= i < sorted.len() ==> s@.to_multiset().contains(sorted[i]));
        s@.to_multiset_ensures();
    }
    // assert-end
    // assert-start
    assert(forall|i: int| #![trigger s[i]] 0 <= i < s.len() ==> sorted@.contains(s[i])) by {
        assert(forall|i: int| #![auto] 0 <= i < s.len() ==> s@.to_multiset().contains(s[i])) by {
            s@.to_multiset_ensures();
        }
        assert(forall|i: int| #![auto] 0 <= i < s.len() ==> sorted@.to_multiset().contains(s[i]));
        sorted@.to_multiset_ensures();
    }
    // assert-end
    unique_sorted(sorted)
    // impl-end
}

}
fn main() {}
