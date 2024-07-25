use vstd::prelude::*;

verus! {

spec fn in_array(a: Seq<i32>, x: i32) -> bool {
    exists|i: int| 0 <= i < a.len() && a[i] == x
}
    
fn in_array_exec(a: &Vec<i32>, x: i32) -> (result: bool) 
    ensures 
        result == in_array(a@, x),
{
    let mut i = 0;
    while i < a.len()
        invariant 
            0 <= i <= a.len(),
            forall|k: int| 0 <= k < i ==> a[k] != x,
    {
        if a[i] == x {
            return true;
        }
        i = i + 1;
    }
    false
}

#[verifier::loop_isolation(false)]
fn remove_duplicates(a: &[i32]) -> (result: Vec<i32>)
    requires
        a.len() >= 1,
    ensures
        forall|i: int| #![auto] 0 <= i < result.len() ==> in_array(a@, result[i]),
        forall|i: int, j: int| 0 <= i < j < result.len() ==> result[i] != result[j],
{
    let mut result: Vec<i32> = Vec::new();
    let mut i = 0;
    while i < a.len()
        invariant
            0 <= i <= a.len(),
            forall|k: int| #![auto] 0 <= k < result.len() ==> in_array(a@, result[k]),
            forall|k: int, l: int| 0 <= k < l < result.len() ==> result[k] != result[l],
    {
        if !in_array_exec(&result, a[i]) {
            result.push(a[i]);
        }
        i = i + 1;
    }
    result
}

fn main() {}
}