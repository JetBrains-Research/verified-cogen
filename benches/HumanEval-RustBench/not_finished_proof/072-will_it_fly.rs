use vstd::prelude::*;

verus! {

proof fn lemma_increasing_sum_params(s: Seq<u32>, i: int, j: int)
    // pre-conditions-start
    requires
        0 <= i <= j <= s.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        spec_sum(s.subrange(0, i)) <= spec_sum(s.subrange(0, j)),
    decreases j - i,
    // post-conditions-end
{
    // impl-start
    if (i < j) {
        assert(spec_sum(s.subrange(0, j - 1)) <= spec_sum(s.subrange(0, j))) by {
            assert(s.subrange(0, j).drop_last() == s.subrange(0, j - 1));
        }
        lemma_increasing_sum_params(s, i, j - 1);
    }
    // impl-end
}
// pure-end

proof fn lemma_increasing_sum(s: Seq<u32>)
    // post-conditions-start
    ensures
        forall|i: int, j: int|
            #![trigger spec_sum(s.subrange(0, i)), spec_sum(s.subrange(0, j))]
            0 <= i <= j <= s.len() ==> spec_sum(s.subrange(0, i)) <= spec_sum(s.subrange(0, j)),
    // post-conditions-end
{
    // impl-start
    assert forall|i: int, j: int|
        #![trigger spec_sum(s.subrange(0, i)), spec_sum(s.subrange(0, j))]
        0 <= i <= j <= s.len() ==> spec_sum(s.subrange(0, i)) <= spec_sum(s.subrange(0, j)) by {
        if (0 <= i <= j <= s.len()) {
            lemma_increasing_sum_params(s, i, j);
        }
    }
    // impl-end
}
// pure-end

spec fn spec_sum(s: Seq<u32>) -> (ret:int) {
    s.fold_left(0, |x: int, y| x + y)
}
// pure-end

fn sum_lesser_than_limit(qs: &Vec<u32>, w: u32) -> (ret: bool)
    // post-conditions-start
    ensures
        ret <==> spec_sum(qs@) <= w,
    // post-conditions-end
{
    // impl-start
    let mut sum: u32 = 0;
    for i in 0..qs.len()
        // invariants-start
        invariant
            sum == spec_sum(qs@.subrange(0, i as int)),
            i <= qs.len(),
            sum <= w,
        // invariants-end
    {
        // assert-start
        proof {
            assert(spec_sum(qs@.subrange(0, i + 1)) <= spec_sum(qs@)) by {
                assert(qs@ == qs@.subrange(0, qs@.len() as int));
                lemma_increasing_sum(qs@);
            }
            assert(spec_sum(qs@.subrange(0, i as int)) + qs[i as int] == spec_sum(
                qs@.subrange(0, i + 1),
            )) by {
                assert(qs@.subrange(0, i + 1).drop_last() == qs@.subrange(0, i as int));
            }
        }
        // assert-end
        let sum_opt = sum.checked_add(qs[i]);
        if sum_opt.is_none() {
            assert(spec_sum(qs@.subrange(0, i + 1)) > u32::MAX >= w); // assert-line
            return false;
        } else {
            sum = sum_opt.unwrap();
            if sum > w {
                assert(spec_sum(qs@.subrange(0, i + 1)) > w); // assert-line
                return false;
            }
        }
    }
    true
    // impl-end
}

fn palindrome(qs: &Vec<u32>) -> (ret: bool)
    // post-conditions-start
    ensures
        ret <==> qs@ =~= qs@.reverse(),
    // post-conditions-end
{
    // impl-start
    let mut ret = true;
    let mut i: usize = 0;
    while i < qs.len() / 2
        // invariants-start
        invariant
            i <= qs@.len() / 2,
            ret <==> qs@.subrange(0, i as int) =~= qs@.subrange(
                qs@.len() - i,
                qs@.len() as int,
            ).reverse(),
        // invariants-end
    {
        // assert-start
        assert(qs@.subrange(qs@.len() - (i + 1), qs@.len() as int).reverse().drop_last()
            =~= qs@.subrange(qs@.len() - i, qs@.len() as int).reverse());
        assert(qs@.subrange(qs@.len() - (i + 1), qs@.len() as int).reverse() =~= qs@.subrange(
            qs@.len() - i,
            qs@.len() as int,
        ).reverse().push(qs@.index(qs@.len() - (i + 1))));
        // assert-end
        if qs[i] != qs[qs.len() - i - 1] {
            ret = false;
        }
        i += 1;
    }
    let ghost fst_half = qs@.subrange(0, (qs@.len() / 2) as int);
    let ghost snd_half = qs@.subrange(qs@.len() - qs@.len() / 2, qs@.len() as int);
    // assert-start
    proof {
        if (qs.len() % 2) == 1 {
            assert(qs@ =~= fst_half + qs@.subrange(
                (qs@.len() / 2) as int,
                qs@.len() - qs@.len() / 2,
            ) + snd_half);
        } else {
            assert(qs@ =~= fst_half + snd_half);
        }
    }
    // assert-end
    ret
    // impl-end
}

fn will_it_fly(qs: &Vec<u32>, w: u32) -> (ret: bool)
    // post-conditions-start
    ensures
        ret <==> qs@ =~= qs@.reverse() && spec_sum(qs@) <= w,
    // post-conditions-end
{
    // impl-start
    palindrome(qs) && sum_lesser_than_limit(qs, w)
    // impl-end
}

}
fn main() {}
