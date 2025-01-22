use vstd::prelude::*;

verus! {

fn derivative(xs: &Vec<usize>) -> (ret: Option<Vec<usize>>)
    // post-conditions-start
    ensures
        ret.is_some() ==> xs@.len() == 0 || xs@.map(|i: int, x| i * x).skip(1)
            =~= ret.unwrap()@.map_values(|x| x as int),
    // post-conditions-end
{
    // impl-start
    let mut ret = Vec::new();
    if xs.len() == 0 {
        return Some(ret);
    }
    let mut i = 1;
    while i < xs.len()
        // invariants-start
        invariant
            xs@.map(|i: int, x| i * x).subrange(1, i as int) =~= ret@.map_values(|x| x as int),
            1 <= i <= xs.len(),
        // invariants-end
    {
        ret.push(xs[i].checked_mul(i)?);

        let ghost prods = xs@.map(|i: int, x| i * x);
        // assert-start
        assert(prods.subrange(1, i as int).push(prods.index(i as int)) =~= prods.subrange(
            1,
            i + 1 as int,
        ));
        // assert-end

        i += 1;
    }
    assert(xs@.map(|i: int, x| i * x).subrange(1, i as int) =~= xs@.map(|i: int, x| i * x).skip(1)); // assert-line
    Some(ret)
    // impl-end
}

}
fn main() {}
