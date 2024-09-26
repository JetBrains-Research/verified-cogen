use vstd::prelude::*;

verus! {

fn binary_search_recursive(v: &[i32], elem: i32, c: isize, f: isize) -> (p: isize)
    // pre-conditions-start
    requires
        v.len() <= 100_000,
        forall|i: int, j: int| 0 <= i < j < v.len() ==> v[i] <= v[j],
        0 <= c <= f + 1 <= v.len(),
        forall|k: int| 0 <= k < c ==> v[k] <= elem,
        forall|k: int| f < k < v.len() ==> v[k] > elem,
    // pre-conditions-end
    // post-conditions-start
    ensures
        -1 <= p < v.len(),
        forall|u: int| 0 <= u <= p ==> v[u] <= elem,
        forall|w: int| p < w < v.len() ==> v[w] > elem,
    // post-conditions-end
    decreases f - c + 1
{
    // impl-start
    if c == f + 1 {
        return c as isize - 1;
    } else {
        let m = ((c + f) as usize / 2) as isize;
        // assert-start
        assert(m < v.len()) by {
            assert(c <= f);
            assert(f < v.len()) by {
                assert(f + 1 <= v.len());
            };
        };
        // assert-end
        if v[m as usize] <= elem {
            return binary_search_recursive(v, elem, m + 1, f);
        } else {
            return binary_search_recursive(v, elem, c, m - 1);
        }
    }
    // impl-end
}


fn main() {}
}
