use vstd::prelude::*;

verus! {

fn monotonic(l: Vec<i32>) -> (ret: bool)
    // post-conditions-start
    ensures
        ret <==> (forall|i: int, j: int| 0 <= i < j < l@.len() ==> l@.index(i) <= l@.index(j)) || (
        forall|i: int, j: int| 0 <= i < j < l@.len() ==> l@.index(i) >= l@.index(j)),
    // post-conditions-end
{
    // impl-start
    if l.len() == 0 || l.len() == 1 {
        return true;
    }
    let mut increasing = true;
    let mut decreasing = true;

    let mut n = 0;
    while n < l.len() - 1
        // invariants-start
        invariant
            l.len() > 1,
            n <= l.len() - 1,
            increasing <==> forall|i: int, j: int|
                0 <= i < j < n + 1 ==> l@.index(i) <= l@.index(j),
            decreasing <==> forall|i: int, j: int|
                0 <= i < j < n + 1 ==> l@.index(i) >= l@.index(j),
        // invariants-end
    {
        if l[n] < l[n + 1] {
            decreasing = false;
        } else if l[n] > l[n + 1] {
            increasing = false;
        }
        n += 1;
    }
    increasing || decreasing
    // impl-end
}

}
fn main() {}
