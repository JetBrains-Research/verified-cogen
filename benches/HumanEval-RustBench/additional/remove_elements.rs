use vstd::prelude::*;

verus! {

spec fn in_array(a: Seq<i32>, x: i32) -> bool {
    exists|i: int| 0 <= i < a.len() && a[i] == x
}

fn in_array_exec(a: &Vec<i32>, x: i32) -> (result: bool)
    // post-conditions-start
    ensures
        result == in_array(a@, x),
    // post-conditions-end
{
    // impl-start
    let mut i = 0;
    while i < a.len()
        // invariants-start
        invariant
            0 <= i <= a.len(),
            forall|k: int| 0 <= k < i ==> a[k] != x,
        // invariants-end
    {
        if a[i] == x {
            return true;
        }
        i = i + 1;
    }
    false
    // impl-end
}

#[verifier::loop_isolation(false)]
fn remove_elements(a: &Vec<i32>, b: &Vec<i32>) -> (c: Vec<i32>)
    // post-conditions-start
    ensures
        forall|k: int| #![auto] 0 <= k < c.len() ==> in_array(a@, c[k]) && !in_array(b@, c[k]),
        forall|i: int, j: int| 0 <= i < j < c.len() ==> c[i] != c[j],
    // post-conditions-end
{
    // impl-start
    let mut c: Vec<i32> = Vec::new();
    let mut i = 0;
    while i < a.len()
        // invariants-start
        invariant
            0 <= i <= a.len(),
            forall|k: int| #![auto] 0 <= k < c.len() ==> in_array(a@, c[k]) && !in_array(b@, c[k]),
            forall|i: int, j: int| 0 <= i < j < c.len() ==> c[i] != c[j],
        // invariants-end
    {
        if !in_array_exec(b, a[i]) && !in_array_exec(&c, a[i]) {
            c.push(a[i]);
        }
        i = i + 1;
    }
    c
    // impl-end
}

fn main() {}
}
