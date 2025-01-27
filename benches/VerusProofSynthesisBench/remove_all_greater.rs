use vstd::prelude::*;

verus!{
fn remove_all_greater(v: Vec<i32>, e: i32) -> (result: Vec<i32>)
    // pre-conditions-start
    requires 
        forall |k1:int,k2:int| 0 <= k1 < k2 < v.len() ==> v[k1] != v[k2],
    // pre-conditions-end
    // post-conditions-start
    ensures
        forall |k:int| 0 <= k < result.len() ==> result[k] <= e && v@.contains(result[k]),
        forall |k:int| 0 <= k < v.len() && v[k] <= e ==> result@.contains(v[k]),
    // post-conditions-end
{  
    // impl-start
    let mut i: usize = 0;
    let vlen = v.len();
    let mut result: Vec<i32> = vec![];
    while (i < v.len()) 
        // invariants-start
        invariant 
            forall |k:int| 0 <= k < result.len() ==> result[k] <= e && v@.contains(result[k]),
            forall |k:int| 0 <= k < i && v[k] <= e ==> result@.contains(v[k]),
        // invariants-end
    {  
        if (v[i] <= e) {
            let ghost old_result = result;
            result.push(v[i]);
            // assert-start
            assert(forall |k:int| 0<= k < old_result.len() ==> old_result[k] == result[k]);
            assert(result[result.len() - 1] == v[i as int]);
            // assert-end
        }
        i = i + 1;
    }  
    result
    // impl-end
}
}

fn main() {}
