use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn max(a: &[i32]) -> (x: usize)
    requires
        a.len() > 0,
    ensures
        0 <= x < a.len(),
        forall|k: int| 0 <= k < a.len() ==> a[k] <= a[x as int],
{
    let mut x = 0;
    let mut y = a.len() - 1;

    let ghost mut m = 0;
    while x != y
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
}

fn main() {}
}
