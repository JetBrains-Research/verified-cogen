use vstd::prelude::*;

verus! {

#[verifier::external_body]
fn swap(a: &mut Vec<bool>, i: usize, j: usize)
    requires
        0 <= i < j < old(a).len(),
    ensures
        a[i as int] == old(a)[j as int],
        a[j as int] == old(a)[i as int],
        forall|k: int| 0 <= k < a.len() && k != i && k != j ==> a[k] == old(a)[k],
        a.len() == old(a).len(),
        a@.to_multiset() =~~= old(a)@.to_multiset(),
{
    let tmp = a[i];
    a.set(i, a[j]);
    a.set(j, tmp);
}

#[verifier::loop_isolation(false)]
fn two_way_sort(a: &mut Vec<bool>)
    requires
        old(a).len() <= 100_000,
    ensures
        a.len() == old(a).len(),
        a@.to_multiset() == old(a)@.to_multiset(),
        forall|i: int, j: int| 0 <= i < j < a.len() ==> !a[i] || a[j],
{
    let mut i = 0isize;
    let mut j = a.len() as isize - 1;
    while i <= j
        invariant
            0 <= i <= j + 1 <= a.len(),
            forall|k: int| 0 <= k < i ==> !a[k],
            forall|k: int| j < k < a.len() ==> a[k],
            a.len() == old(a).len(),
            a@.to_multiset() == old(a)@.to_multiset(),
    {
        if !a[i as usize] {
            i = i + 1;
        } else if a[j as usize] {
            j = j - 1;
        } else {
            swap(a, i as usize, j as usize);
            i = i + 1;
            j = j - 1;
        }
    }
}

fn main() {}
}
