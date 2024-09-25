use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn max_dafny_lsp(a: &[i32]) -> (x: usize)
    // pre-conditions-start
    requires
        a.len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        0 <= x < a.len(),
        forall|k: int| 0 <= k < a.len() ==> a[k] <= a[x as int],
    // post-conditions-end
{
    // impl-start
    let mut x = 0;
    let mut y = a.len() - 1;

    let ghost mut m = 0;
    while x != y
        // invariants-start
        invariant
            0 <= x <= y < a.len(),
            m == x || m == y,
            forall|i: int| 0 <= i < x ==> a[i] <= a[m],
            forall|i: int| y < i < a.len() ==> a[i] <= a[m],
        // invariants-end
    {
        if a[x] <= a[y] {
            x = x + 1;
            proof {
                m = y as int;
            }
        } else {
            y = y - 1;
            proof {
                m = x as int;
            }
        }
    }
    x
    // impl-end
}

fn main() {}
}
