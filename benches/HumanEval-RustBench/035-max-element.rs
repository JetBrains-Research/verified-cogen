use vstd::prelude::*;

verus! {

fn max_element(a: &Vec<i32>) -> (max: i32)
    requires
        a.len() > 0,
    ensures
        forall|i: int| 0 <= i < a.len() ==> a[i] <= max,
        exists|i: int| 0 <= i < a.len() && a[i] == max,
{
    let mut max = a[0];
    for i in 1..a.len()
        invariant
            forall|j: int| 0 <= j < i ==> a[j] <= max,
            exists|j: int| 0 <= j < i && a[j] == max,
    {
        if a[i] > max {
            max = a[i];
        }
    }
    max
}

} 
fn main() {}
