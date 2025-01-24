use vstd::prelude::*;

verus! {

spec fn spec_sum_to_n(n: nat) -> (ret:nat)
    decreases n,
{
    if (n == 0) {
        0
    } else {
        n + spec_sum_to_n((n - 1) as nat)
    }
}
// pure-end

fn sum_to_n(n: u32) -> (sum: Option<u32>)
    // post-conditions-start
    ensures
        sum.is_some() ==> sum.unwrap() == spec_sum_to_n(n as nat),
    // post-conditions-end
{
    // impl-start
    let mut res: u32 = 0;
    let mut sum: u32 = 0;
    let mut i: u32 = 0;
    while i < n
        // invariants-start
        invariant
            i <= n,
            res == spec_sum_to_n(i as nat),
            res <= u32::MAX,
        // invariants-end
    {
        i += 1;
        res = i.checked_add(res)?;
    }
    Some(res)
    // impl-end
}

}
fn main() {}
