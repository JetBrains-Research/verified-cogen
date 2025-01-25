use vstd::prelude::*;
fn main() {}
verus!{
fn myfun2(x: &mut Vec<i32>) 
    // pre-conditions-start
    requires 
        forall |k:int| 0 <= k < old(x).len() ==> old(x)[k] <= 0x7FFF_FFFB,
    // pre-conditions-end
    // post-conditions-start
    ensures 
        x@.len() == old(x)@.len(),
        forall |k:int| 0 <= k < x.len() ==> #[trigger] x@[k] == old(x)@[k] + 4,
    // post-conditions-end
{
    // impl-start
    let mut i: usize = 0;
    let xlen: usize = x.len();
    while (i < xlen) 
        // invariants-start
        invariant 
            xlen == x.len(),  
            forall |k:int| 0 <= k < i ==> #[trigger] x[k] == old(x)[k] + 4,
            forall |k:int| i <= k < xlen ==> x[k] == old(x)[k],
            forall |k:int| 0 <= k < xlen ==> old(x)[k] <= 0x7FFF_FFFB,
        // invariants-end
    { 
        x.set(i, x[i] + 4);  
        i = i + 1;
    }  
    // impl-end
}
}
