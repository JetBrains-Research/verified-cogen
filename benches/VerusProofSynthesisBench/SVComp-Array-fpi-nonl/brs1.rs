use vstd::prelude::*;
fn main() {}

verus!{

fn myfun(a: &mut Vec<i32>, sum: &mut Vec<i32>, N: i32)
    // pre-conditions-start
    requires
        N > 0,
        old(a).len() == N,
        old(sum).len() == 1,
    // pre-conditions-end
    // post-conditions-start
    ensures
        sum[0] <= N,
    // post-conditions-end
{
    // impl-start
    let mut i: usize = 0;
    while (i < N as usize)
        // invariants-start
        invariant
            a.len() == N,
            forall |k:int| 0 <= k < i ==> a[k] == 1,
        // invariants-end
    {
        if (i % 1 == 0) {
            a.set(i, 1);
        } else {
            a.set(i, 0);
        }
        i = i + 1;
    }

    i = 0;
    while (i < N as usize)
        // invariants-start
        invariant
            i <= N as usize,
            sum.len() == 1,
            a.len() == N,
            i > 0 ==> sum[0] <= i,
            forall |k:int| 0 <= k < N ==> a[k] == 1,
        // invariants-end
    {
        if (i == 0) {
            sum.set(0, 0);
        } else {
            sum.set(0, sum[0] + a[i]);
        }
        i = i + 1;
    }
    // impl-end
}
}
