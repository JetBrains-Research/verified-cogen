use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn last_position(a: &[i32], elem: i32) -> (result: usize)
    requires
        0 < a.len() < 100_000,
        exists|i: int| 0 <= i < a.len() && a[i] == elem,
    ensures
        0 <= result < a.len(),
        forall|i: int| result < i < a.len() ==> a[i] != elem,
        a[result as int] == elem,
{
    let mut i = a.len() as isize - 1;
    while i >= 0
        invariant
            0 <= i + 1 <= a.len() as isize,
            forall|k: int| i < k < a.len() ==> a[k] != elem,
    {
        if a[i as usize] == elem {
            return i as usize;
        }
        i = i - 1;
    }
    a.len()
}

fn main() {}
}
