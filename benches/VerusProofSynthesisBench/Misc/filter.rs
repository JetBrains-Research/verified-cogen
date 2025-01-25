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
        y@ == x@.filter(|k:u64| k%3 == 0),
    // post-conditions-end
{
    // impl-start
    let mut i: usize = 0;
    let xlen = x.len();
    
    // assert-start
    assert(y@ == x@.take(0).filter(|k:u64| k%3 ==0)); 
    // assert-end
    while (i < xlen) 
        // invariants-start
        invariant 
            0 <= i <= xlen,
            x@.len() == xlen,  
            y@ == x@.take(i as int).filter(|k:u64| k%3 == 0),
        // invariants-end
    { 
        if (x[i] % 3 == 0) {
            y.push(x[i]);
        }
        // assert-start
        assert(x@.take((i + 1) as int).drop_last() == x@.take(i as int));
        reveal(Seq::filter);
        // assert-end
        i = i + 1;
    }
    // assert-start
    assert(x@ == x@.take(x.len() as int)); 
    // assert-end
    // impl-end
}
}
