use vstd::prelude::*;
fn main() {}
verus!{
fn simple_nested(a: &mut Vec<i32>, b: &Vec<i32>, N: i32) -> (sum: i32)
    // pre-conditions-start
    requires 
        forall |k:int| k <= #[trigger] b[k] <= k + 1,
        old(a).len() == N,
        b.len() == N,
        N <= 0x3FFF_FFFF,
    // pre-conditions-end
    // post-conditions-start
    ensures
        N <= sum <= 2*N,
    // post-conditions-end
{  
    let mut i: usize = 0;
    let mut sum: i32 = 0;
    while (i < N as usize) 
        // invariants-start
        invariant 
            0 <= i <= N,
            N <= 0x3FFF_FFFF,
            a.len() == N, 
            b.len() == N, 
            forall |k:int| k <= #[trigger] b[k] <= k + 1,
            i <= sum <= 2*i,
        // invariants-end
    {  
        a.set(i, b[i] + 1);
        let mut j: usize = 0;
        while (j < i)
            // invariants-start
            invariant 
                0 <= i < N,
                0 <= j <= i,
                a.len() == N,  
                i + 1 - j <= a[i as int] <= i + 2 - j,
            // invariants-end
        {
            a.set(i, a[i] - 1);
            j = j + 1;
        }
        sum = sum + a[i];
        i = i + 1;
    }  
    sum
    // impl-end
}
}
