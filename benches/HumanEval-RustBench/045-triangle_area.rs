use vstd::prelude::*;

verus! {

fn triangle_area(a: u64, h: u64) -> (area: u64)
    // pre-conditions-start
    requires
        a > 0,
        h > 0,
        a * h / 2 <= u64::MAX
        ,
    // pre-conditions-end
    // post-conditions-start
    ensures
        area == a * h / 2,
    // post-conditions-end
{
    // impl-start
    if a % 2 == 0 {
        assert(a % 2 == 0 ==> (a / 2) * h == a * h / 2) by (nonlinear_arith); // assert-line
        (a / 2) * h
    } else {
        assert(a % 2 == 1 ==> (a / 2) * h + (h / 2) == a * h / 2) by (nonlinear_arith); // assert-line
        (a / 2) * h + (h / 2)
    }
    // impl-end
}

}
fn main() {}
