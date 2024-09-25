use vstd::prelude::*;

verus! {

fn add(x: i32, y: i32) -> (res: Option<i32>)
    ensures
        res.is_some() ==> res.unwrap() == x + y,
{
    x.checked_add(y)
}

} 
fn main() {}
