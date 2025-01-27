use vstd::prelude::*;

verus!{
fn choose_odd(v: &Vec<u64>) -> (odd_index: usize)
    // pre-conditions-start
    requires    
        exists |q:int| 0 <= q < v.len() && v[q] % 2 == 1,
    // pre-conditions-end
    // post-conditions-start
    ensures
        odd_index < v.len(),
    // post-conditions-end
{
    // impl-start
    let mut j: usize = 0;
    
    while (j < v.len())
        // invariants-start
        invariant 
            forall |q:int| 0<=q<j ==> #[trigger] v[q]%2!=1,
        // invariants-end
    {
        if (v[j] % 2 == 1) {
            return j;
        }
        j = j + 1;
    }
    j
    // impl-end
}
}


fn main() {}