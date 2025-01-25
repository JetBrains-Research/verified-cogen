use vstd::prelude::*;
fn main() {}

verus!{
fn myfun4(x: &Vec<u64>, y: &mut Vec<u64>)
    // pre-conditions-start
    requires 
        old(y).len() == 0,
    // pre-conditions-end
    // post-conditions-start
    ensures 
        forall |k:int| 0 <= k < y.len() ==> y[k] % 3 == 0 && x@.contains(y@[k]),
    // post-conditions-end
{
    // impl-start
    let mut i: usize = 0;
    let xlen = x.len();
    
    while (i < xlen) 
        // invariants-start
        invariant 
            x@.len() == xlen, 
            forall |k:int| 0 <= k < y.len() ==> y[k] % 3 == 0 && x@.contains(y@[k]),
        // invariants-end
    { 
        if (x[i] % 3 == 0) {
            y.push(x[i]);
        }
        i = i + 1;
    }
    // impl-end
}
}
