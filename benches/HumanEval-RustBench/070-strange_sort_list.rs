use vstd::calc;
use vstd::prelude::*;
use vstd::seq_lib::lemma_multiset_commutative;

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
fn strange_sort_list_helper(s: &Vec<i32>) -> (ret: (Vec<i32>, Vec<i32>))
    // post-conditions-start
    ensures
        s@.to_multiset() == (ret.0)@.to_multiset(),
        s@.len() == (ret.0)@.len() == (ret.1)@.len(),
        forall|i: int|
            0 <= i < s@.len() && i % 2 == 0 ==> (ret.1)@.index(i) == (ret.0)@.index(i / 2),
        forall|i: int|
            0 <= i < s@.len() && i % 2 == 1 ==> (ret.1)@.index(i) == (ret.0)@.index(
                s@.len() - (i - 1) / 2 - 1,
            ),
    // post-conditions-end
{
    // impl-start
    let sorted = sort_seq(s);
    let mut strange = Vec::new();
    let mut i: usize = 0;
    while i < sorted.len()
        // invariants-start
        invariant
            i <= sorted.len() == s@.len(),
            strange@.len() == i,
            forall|j: int| 0 <= j < i && j % 2 == 0 ==> strange@.index(j) == sorted@.index(j / 2),
            forall|j: int|
                0 < j < i && j % 2 == 1 ==> strange@.index(j) == sorted@.index(
                    sorted@.len() - (j / 2) - 1,
                ),
        // invariants-end
    {
        if i % 2 == 0 {
            strange.push(sorted[i / 2]);
        } else {
            let r = (i - 1) / 2;
            strange.push(sorted[s.len() - r - 1]);
        }
        i += 1;
    }
    (sorted, strange)
    // impl-end
}

fn strange_sort_list(s: &Vec<i32>) -> (ret: Vec<i32>)
    // post-conditions-start
    ensures
        s@.len() == ret@.len(),
    // post-conditions-end
{
    // impl-start
    let (_, strange) = strange_sort_list_helper(s);
    strange
    // impl-end
}

}
fn main() {}
