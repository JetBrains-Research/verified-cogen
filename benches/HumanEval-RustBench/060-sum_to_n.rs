use vstd::prelude::*;

verus! {

spec fn spec_sum_to_n(n: nat) -> nat
    decreases n,
{
    if (n == 0) {
        0
    } else {
        n + spec_sum_to_n((n - 1) as nat)
    }
}

fn sum_to_n(n: u32) -> (sum: Option<u32>)
    ensures
        sum.is_some() ==> sum.unwrap() == spec_sum_to_n(n as nat),
{
    let mut res: u32 = 0;
    let mut sum: u32 = 0;
    let mut i: u32 = 0;
    while i < n
        invariant
            i <= n,
            res == spec_sum_to_n(i as nat),
            res <= u32::MAX,
    {
        i += 1;
        res = i.checked_add(res)?;
    }
    Some(res)
}

} 
fn main() {}
