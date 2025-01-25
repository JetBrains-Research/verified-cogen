use vstd::prelude::*;
fn main() {}

verus!{
proof fn lemma_seq_take_ascend<T>(v: Seq<T>, i: int)
    // pre-conditions-start
    requires
        0 < i <= v.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        v.take(i as int).drop_last() == v.take(i-1),
    // post-conditions-end
{
    // impl-start
    assert(v.take(i as int).drop_last() =~= v.take(i-1));
    // impl-end
}
// pure-end

proof fn lemma_seq_take_all<T>(v: Seq<T>)
    // post-conditions-start
    ensures
        v == v.take(v.len() as int),
    // post-conditions-end
{
    // impl-start
    assert(v =~= v.take(v.len() as int));
    // impl-end
}
// pure-end

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
        proof{
            lemma_seq_take_ascend(x@, i+1);
            reveal(Seq::filter);//routine for filter
        }
        // assert-end
        i = i + 1;
    }
    // assert-start
    proof{
        lemma_seq_take_all(x@);
    }
    // assert-end
    // impl-end
}
}
