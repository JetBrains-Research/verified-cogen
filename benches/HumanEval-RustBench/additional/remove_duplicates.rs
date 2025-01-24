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
fn remove_duplicates(a: &[i32]) -> (result: Vec<i32>)
    // pre-conditions-start
    requires
        a.len() >= 1,
    // pre-conditions-end
    // post-conditions-start
    ensures
        forall|i: int| #![auto] 0 <= i < result.len() ==> in_array(a@, result[i]),
        forall|i: int, j: int| 0 <= i < j < result.len() ==> result[i] != result[j],
    // post-conditions-end
{
    // impl-start
    let mut result: Vec<i32> = Vec::new();
    let mut i = 0;
    while i < a.len()
        // invariants-start
        invariant
            0 <= i <= a.len(),
            forall|k: int| #![auto] 0 <= k < result.len() ==> in_array(a@, result[k]),
            forall|k: int, l: int| 0 <= k < l < result.len() ==> result[k] != result[l],
        // invariants-end
    {
        if !in_array_exec(&result, a[i]) {
            result.push(a[i]);
        }
        i = i + 1;
    }
    result
    // impl-end
}

fn main() {}
}
