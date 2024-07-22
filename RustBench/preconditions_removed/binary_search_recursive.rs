use vstd::prelude::*;

verus! {

fn binary_search_recursive(v: &[i32], elem: i32, c: isize, f: isize) -> (p: isize)
    ensures
        -1 <= p < v.len(),
        forall|u: int| 0 <= u <= p ==> v[u] <= elem,
        forall|w: int| p < w < v.len() ==> v[w] > elem,
    decreases f - c + 1
{
    if c == f + 1 {
        return c as isize - 1;
    } else {
        let m = ((c + f) as usize / 2) as isize;
        assert(m < v.len()) by {
            assert(c <= f);
            assert(f < v.len()) by { 
                assert(f + 1 <= v.len());
            };
        };
        if v[m as usize] <= elem {
            return binary_search_recursive(v, elem, m + 1, f);
        } else {
            return binary_search_recursive(v, elem, c, m - 1);  
        }
    }
}


fn main() {}
}