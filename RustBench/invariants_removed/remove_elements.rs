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
    {
        if a[i] == x {
            return true;
        }
        i = i + 1;
    }
    false
}

#[verifier::loop_isolation(false)]
fn remove_elements(a: &Vec<i32>, b: &Vec<i32>) -> (c: Vec<i32>)
    ensures
        forall|k: int| #![auto] 0 <= k < c.len() ==> in_array(a@, c[k]) && !in_array(b@, c[k]),
        forall|i: int, j: int| 0 <= i < j < c.len() ==> c[i] != c[j],
{
    let mut c: Vec<i32> = Vec::new();
    let mut i = 0;
    while i < a.len()
    {
        if !in_array_exec(b, a[i]) && !in_array_exec(&c, a[i]) {
            c.push(a[i]);
        }
        i = i + 1;
    }
    c
}

fn main() {}
}
