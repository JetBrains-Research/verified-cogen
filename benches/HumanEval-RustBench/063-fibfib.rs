use vstd::prelude::*;

verus! {

spec fn spec_fibfib(n: nat) -> (ret: nat)
    decreases n,
{
    if (n == 0) {
        0
    } else if (n == 1) {
        0
    } else if (n == 2) {
        1
    } else {
        spec_fibfib((n - 1) as nat) + spec_fibfib((n - 2) as nat) + spec_fibfib((n - 3) as nat)
    }
}
// pure-end

fn fibfib(x: u32) -> (ret: Option<u32>)
    // post-conditions-start
    ensures
        ret.is_some() ==> spec_fibfib(x as nat) == ret.unwrap(),
    // post-conditions-end
{
    // impl-start
    match (x) {
        0 => Some(0),
        1 => Some(0),
        2 => Some(1),
        _ => fibfib(x - 1)?.checked_add(fibfib(x - 2)?)?.checked_add(fibfib(x - 3)?),
    }
    // impl-end
}

}
fn main() {}
