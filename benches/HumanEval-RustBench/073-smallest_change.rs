use vstd::prelude::*;

verus! {

spec fn zip_halves<T>(v: Seq<T>) -> (ret: Seq<(T, T)>) {
    v.take((v.len() / 2) as int).zip_with(v.skip(((v.len() + 1) / 2) as int).reverse())
}

spec fn diff(s: Seq<(i32, i32)>) -> int {
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

fn smallest_change(v: Vec<i32>) -> (change: usize)
    requires
        v@.len() < usize::MAX,
    ensures
        change == diff(zip_halves(v@)),
{
    let mut ans: usize = 0;
    let ghost zipped = Seq::<(i32, i32)>::empty();
    for i in 0..v.len() / 2
        invariant
            ans <= i <= v@.len() / 2 < usize::MAX,
            ans == diff(zipped),
            zipped =~= zip_halves(v@).take(i as int),
    {
        proof {
            let ghost pair = (v[i as int], v[v.len() - i - 1]);
            let ghost zipped_old = zipped;
            zipped = zipped.push(pair);
            assert(zipped.drop_last() =~= zipped_old);
        }
        if v[i] != v[v.len() - i - 1] {
            ans += 1;
        }
    }
    assert(zip_halves(v@).take((v@.len() / 2) as int) =~= zip_halves(v@));
    ans
}

} 
fn main() {}
