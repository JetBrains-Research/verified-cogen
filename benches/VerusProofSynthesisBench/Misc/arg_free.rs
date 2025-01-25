use vstd::prelude::*;

verus!{
fn choose_odd()
{
    // impl-start
    let mut idx: u64 = 0;
    let mut res: u64 = 5;
    
    let ghost gap = res-idx;
    
    while (idx < 10)
        // invariants-start
        invariant
            idx<=10,
            gap<100,
            gap==res-idx,
        // invariants-end
    {
        res = res + 1;
        idx = idx + 1;
    }
    idx = 0;
    
    let ghost gap = res - idx;
   
    while (idx < 10)
        // invariants-start
        invariant
            idx<=10,
            gap<100,
            gap==res-idx,
        // invariants-end
    {
        res = res + 1;
        idx = idx + 1;
    }
    // assert-start
    assert(res == 25);
    // assert-end
    // impl-end
}
}
fn main() {}
