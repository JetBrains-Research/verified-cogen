use vstd::prelude::*;

verus! {

#[verifier::external_body]
fn swap(a: &mut Vec<bool>, i: usize, j: usize)
    // pre-conditions-start
    requires
        0 <= i < j < old(a).len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        a[i as int] == old(a)[j as int],
        a[j as int] == old(a)[i as int],
        forall|k: int| 0 <= k < a.len() && k != i && k != j ==> a[k] == old(a)[k],
        a.len() == old(a).len(),
        a@.to_multiset() =~~= old(a)@.to_multiset(),
    // post-conditions-end
{
    // impl-start
    let tmp = a[i];
    a.set(i, a[j]);
    a.set(j, tmp);
    // impl-end
}

#[verifier::loop_isolation(false)]
fn two_way_sort(a: &mut Vec<bool>)
    // pre-conditions-start
    requires
        old(a).len() <= 100_000,
    // pre-conditions-end
    // post-conditions-start
    ensures
        a.len() == old(a).len(),
        a@.to_multiset() == old(a)@.to_multiset(),
        forall|i: int, j: int| 0 <= i < j < a.len() ==> !a[i] || a[j],
    // post-conditions-end
{
    // impl-start
    let mut i = 0isize;
    let mut j = a.len() as isize - 1;
    while i <= j
        // invariants-start
        invariant
            0 <= i <= j + 1 <= a.len(),
            forall|k: int| 0 <= k < i ==> !a[k],
            forall|k: int| j < k < a.len() ==> a[k],
            a.len() == old(a).len(),
            a@.to_multiset() == old(a)@.to_multiset(),
        // invariants-end
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
    // impl-end
}

fn main() {}
}
