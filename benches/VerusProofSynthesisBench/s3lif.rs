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
            forall |j: int| 0<= j < i ==> a[j] == 1,
            a.len() == N,
        // invariants-end
    {
        a.set(i, 1);
        i = i + 1;
    }

    i = 0;
    while (i < N as usize)
        // invariants-start
        invariant
            forall |j: int| 0<= j < i ==> a[j] == 4,
            forall |j: int| i <= j < N ==> a[j] == 1,
            a.len() == N,
        // invariants-end
    {
        if (a[i] == 1) {
            a.set(i, a[i] + 3);
        } else {
            a.set(i, a[i] - 1);
        }
        i = i + 1;
    }

    i = 0;
    while (i < N as usize)
        // invariants-start
        invariant
            i <= N,
            forall |j: int| 0<= j < N ==> a[j] == 4,
            a.len() == N,
            sum.len() == 1,
            sum[0] == 4 * i,
            N <= 1000,
        // invariants-end
    {
        sum.set(0, sum[0] + a[i]);
        i = i + 1;
    }
    // impl-end
}
}

fn main() {}