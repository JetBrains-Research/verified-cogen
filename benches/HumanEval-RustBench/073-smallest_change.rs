use vstd::prelude::*;

verus! {

spec fn zip_halves<T>(v: Seq<T>) -> (ret: Seq<(T, T)>) {
    v.take((v.len() / 2) as int).zip_with(v.skip(((v.len() + 1) / 2) as int).reverse())
}
// pure-end

spec fn diff(s: Seq<(i32, i32)>) -> (ret: int) {
    s.fold_left(
        0,
        |acc: int, x: (i32, i32)|
            if (x.0 != x.1) {
                acc + 1
            } else {
                acc
            },
    )
}
// pure-end

fn smallest_change(v: Vec<i32>) -> (change: usize)
    // pre-conditions-start
    requires
        v@.len() < usize::MAX,
    // pre-conditions-end
    // post-conditions-start
    ensures
        change == diff(zip_halves(v@)),
    // post-conditions-end
{
    // impl-start
    let mut ans: usize = 0;
    let ghost zipped = Seq::<(i32, i32)>::empty();
    for i in 0..v.len() / 2
        // invariants-start
        invariant
            ans <= i <= v@.len() / 2 < usize::MAX,
            ans == diff(zipped),
            zipped =~= zip_halves(v@).take(i as int),
        // invariants-end
    {
        // assert-start
        proof {
            let ghost pair = (v[i as int], v[v.len() - i - 1]);
            let ghost zipped_old = zipped;
            zipped = zipped.push(pair);
            assert(zipped.drop_last() =~= zipped_old);
        }
        // assert-end
        if v[i] != v[v.len() - i - 1] {
            ans += 1;
        }
    }
    assert(zip_halves(v@).take((v@.len() / 2) as int) =~= zip_halves(v@)); // assert-line
    ans
    // impl-end
}

}
fn main() {}
