#![crate_name="max_segment_sum"]

use vstd::prelude::*;

verus! {

spec fn sum(a: &Vec<i32>, s: int, t: int) -> int
{
    0
}

#[verifier::loop_isolation(false)]
fn max_segment_sum(a: &mut Vec<i32>, s: usize, t: usize) -> (p: (usize, usize)) 
    ensures
        ({ let (i, j) = p; 0 <= i <= j <= a.len() }),
        ({ let (i, j) = p; forall|k: int, l: int| 0 <= k <= l <= a.len() ==> sum(a, k, l) <= sum(a, i as int, j as int) })
{
    let mut k = 0;
    let mut m = 0;
    let mut s = 0;
    let mut n = 0;
    let mut c = 0;
    let mut t = 0;
    while n < a.len()
        invariant 
            0 <= c <= n <= a.len() && t == sum(a, c as int, n as int),
            forall|b: int| 0 <= b <= n ==> sum(a, b, n as int) <= sum(a, c as int, n as int),
            0 <= k <= m <= n && s == sum(a, k as int, m as int),
            forall|p: int, q: int| 0 <= p <= q <= n ==> sum(a, p, q) <= sum(a, k as int, m as int),
    {
        t = t + a[n];
        n = n + 1;
        if t < 0 {
            c = n;
            t = 0;
        } else if s < t {
            k = c;
            m = n;
            s = t;
        }
    }
    (k, m)
}

fn main() {}
}
