use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn replace(a: &mut Vec<i32>, x: i32, y: i32)
    ensures
        a.len() == old(a).len(),
        forall|k: int| 0 <= k < old(a).len() && old(a)[k] == x ==> a[k] == y,
        forall|k: int| 0 <= k < old(a).len() && old(a)[k] != x ==> a[k] == old(a)[k],
{
    let mut i = 0;
    while i < a.len()
        invariant
            0 <= i <= a.len(),
            a.len() == old(a).len(),
            forall|k: int| 0 <= k < i && old(a)[k] == x ==> a[k] == y,
            forall|k: int| 0 <= k < i && old(a)[k] != x ==> a[k] == old(a)[k],
            forall|k: int| i <= k < a.len() ==> a[k] == old(a)[k],
    {
        if a[i] == x {
            a.set(i, y);
        }
        i = i + 1;
    }
}

fn main() {}
}
