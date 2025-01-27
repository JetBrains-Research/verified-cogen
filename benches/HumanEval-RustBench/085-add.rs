use vstd::prelude::*;

verus! {

spec fn odd_or_zero(x: u32) -> (ret:u32) {
    if x % 2 == 0 {
        x
    } else {
        0
    }
}
// pure-end

spec fn add_odd_evens(lst: Seq<u32>) -> (ret:int)
    decreases lst.len(),
{
    if (lst.len() < 2) {
        0
    } else {
        odd_or_zero(lst[1]) + add_odd_evens(lst.skip(2))
    }
}
// pure-end

fn add(lst: Vec<u32>) -> (sum: u64)
    // pre-conditions-start
    requires
        0 < lst.len() < u32::MAX,
    // pre-conditions-end
    // post-conditions-start
    ensures
        sum == add_odd_evens(lst@),
    // post-conditions-end
{
    // impl-start
    let mut sum: u64 = 0;
    let mut i = 1;
    // assert-start
    proof {
        assert(lst@ =~= lst@.skip(0));
    }
    // assert-end
    while (i < lst.len())
        // invariants-start
        invariant
            1 <= i <= lst.len() + 1,
            0 < lst.len() < u32::MAX,
            sum <= (u32::MAX) * i,
            sum == add_odd_evens(lst@) - add_odd_evens(lst@.skip(i - 1 as int)),
        // invariants-end
    {
        if (lst[i] % 2 == 0) {
            sum += lst[i] as u64;
        }
        // assert-start
        proof {
            assert(lst@.skip(i - 1 as int).skip(2) =~= lst@.skip(i + 1 as int));
        }
        // assert-end
        i += 2;
    }
    return sum;
    // impl-end
}

} // verus!
fn main() {}
