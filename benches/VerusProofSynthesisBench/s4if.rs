use vstd::prelude::*;

verus!{
fn myfun(a: &mut Vec<i32>, sum: &mut Vec<i32>, N: i32)
    // pre-conditions-start
    requires
        N > 0,
        old(a).len() == N,
        old(sum).len() == 1,
        N < 1000,
    // pre-conditions-end
    // post-conditions-start
    ensures
        sum[0] == 4 * N,
    // post-conditions-end
{
    // impl-start
    sum.set(0, 0);
    let mut i: usize = 0;
    while (i < N as usize)
        // invariants-start
        invariant
            forall |k:int| 0<= k < i ==> a[k] == 4,
            a.len() == N,
        // invariants-end
    {
        a.set(i, 4);
        i = i + 1;
    }

    i = 0;
    while (i < N as usize)
        // invariants-start
        invariant
            i <= N,
            forall |k:int| 0<= k < N ==> a[k] == 4,
            a.len() == N,
            sum[0] == 4 * i,
            sum.len() == 1,
            N < 1000,
        // invariants-end
    {
        if (a[i] == 4) {
            sum.set(0, sum[0] + a[i]);
        } else {
            sum.set(0, sum[0] * a[i]);
        }
        i = i + 1;
    }
    // impl-end
}
}

fn main() {}