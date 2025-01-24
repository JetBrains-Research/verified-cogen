use vstd::arithmetic::mul::*;
use vstd::math::abs;
use vstd::prelude::*;

verus! {

proof fn lemma_cube_increases_helper(i: int)
    // post-conditions-start
    ensures
        i >= 0 ==> (i * i * i) <= (i + 1) * (i + 1) * (i + 1),
    // post-conditions-end
{
    // impl-start
    broadcast use group_mul_properties;

    if (i > 0) {
        assert((i + 1) * (i + 1) * (i + 1) == i * i * i + 3 * i * i + 3 * i + 1); // assert-line
        assert(i * i * i + 3 * i * i + 3 * i + 1 > i * i * i); // assert-line
    }
    // impl-end
}
// pure-end

proof fn lemma_cube_increases_params(i: int, j: int)
    // post-conditions-start
    ensures
        0 <= i <= j ==> (i * i * i) <= (j * j * j),
    // post-conditions-end
    decreases j - i,
{
    // impl-start
    if (i == j) {
    }
     else if (i < j) {
        lemma_cube_increases_params(i, j - 1);
        lemma_cube_increases_helper(j - 1);

    }
    // impl-end
}
// pure-end

proof fn lemma_cube_increases()
    // post-conditions-start
    ensures
        forall|i: int, j: int| 0 <= i <= j ==> #[trigger] (i * i * i) <= #[trigger] (j * j * j),
    // post-conditions-end
{
    // impl-start
    assert forall|i: int, j: int|
        0 <= i <= j ==> #[trigger] (i * i * i) <= #[trigger] (j * j * j) by {
        lemma_cube_increases_params(i, j);
    }
    // impl-end
}
// pure-end

fn checked_cube(x: i32) -> (ret: Option<i32>)
    // pre-conditions-start
    requires
        x >= 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        ret.is_some() ==> ret.unwrap() == x * x * x,
        ret.is_none() ==> x * x * x > i32::MAX,
    // post-conditions-end
{
    // impl-start
    if x == 0 {
        return Some(0);
    }
    let sqr = x.checked_mul(x);
    if sqr.is_some() {
        let cube = sqr.unwrap().checked_mul(x);
        if cube.is_some() {
            let ans = cube.unwrap();
            assert(ans == x * x * x); // assert-line
            Some(ans)
        } else {
            assert(x * x * x > i32::MAX); // assert-line
            None
        }
    } else {
        assert(x > 0); // assert-line
        assert(x * x > i32::MAX); // assert-line
        // assert-start
        proof {
            lemma_mul_increases(x as int, x * x);
        }
        // assert-end
        assert(x * x * x >= x * x); // assert-line
        None
    }
    // impl-end
}

#[verifier::external_fn_specification]
fn ex_abs(x: i32) -> (ret: i32)
    requires
        x != i32::MIN,

    ensures
        ret == abs(x as int),
{
    x.abs()
}

fn is_cube(x: i32) -> (ret: bool)
    // pre-conditions-start
    requires
        x != i32::MIN,
    // pre-conditions-end
    // post-conditions-start
    ensures
        ret <==> exists|i: int| 0 <= i && abs(x as int) == #[trigger] (i * i * i),
    // post-conditions-end
{
    // impl-start
    let x_abs = x.abs();
    if x_abs == 0 {
        assert(abs(x as int) == 0 * 0 * 0); // assert-line
        return true;
    } else if (x_abs == 1) {
        assert(abs(x as int) == 1 * 1 * 1); // assert-line
        return true;
    }
    assert(-1 > x || x > 1); // assert-line
    let mut i = 2;
    while i < x_abs
        // invariants-start
        invariant
            forall|j: int| 2 <= j < i ==> abs(x as int) != #[trigger] (j * j * j),
            2 <= i <= abs(x as int) == x_abs,
        // invariants-end
    {
        let prod = checked_cube(i);
        if prod.is_some() && prod.unwrap() == x.abs() {
            return true;
        }
        i += 1;
    }
    // assert-start
    assert(forall|j: int| 2 <= j ==> abs(x as int) != #[trigger] (j * j * j)) by {
        assert(forall|j: int| 2 <= j < i ==> abs(x as int) != #[trigger] (j * j * j));

        assert(forall|j: int| i <= j ==> abs(x as int) < #[trigger] (j * j * j)) by {
            assert(abs(x as int) < #[trigger] (i * i * i)) by {
                broadcast use group_mul_properties;

                assert(i <= i * i <= i * i * i);
            }
            lemma_cube_increases();
            assert(forall|j: int| i <= j ==> (i * i * i) <= #[trigger] (j * j * j));
        }
    }
    // assert-end
    false
    // impl-end
}

}
fn main() {}
