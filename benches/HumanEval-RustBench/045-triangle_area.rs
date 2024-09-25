use vstd::prelude::*;

verus! {

fn triangle_area(a: u64, h: u64) -> (area: u64)
    requires
        a > 0,  
        h > 0,  
        a * h / 2 <= u64::MAX  
        ,
    ensures
        area == a * h / 2,  
{
    if a % 2 == 0 {
        assert(a % 2 == 0 ==> (a / 2) * h == a * h / 2) by (nonlinear_arith);
        (a / 2) * h
    } else {
        assert(a % 2 == 1 ==> (a / 2) * h + (h / 2) == a * h / 2) by (nonlinear_arith);
        (a / 2) * h + (h / 2)
    }
}

} 
fn main() {}
