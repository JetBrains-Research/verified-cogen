#[allow(unused_imports)]
use vstd::prelude::*;

fn main() {}

verus!{
spec fn f(seq: Seq<u64>, i: int) -> (result: bool) {
    seq[i] == i + 2
}
// pure-end

fn get_element_check_property(arr: Vec<u64>, i: usize) -> (ret: u64)
    // pre-conditions-start
    requires
        arr.len() > 0,
        0 < i < arr@.len(),
        forall |i: int| f(arr@, i),
    // pre-conditions-end
    // post-conditions-start
    ensures
        ret == i + 2,
        ret == arr@[i as int],
    // post-conditions-end
{
    // assert-start
    proof {
        assert(f(arr@, i as int));
    }
    // assert-end
    arr[i]
    // impl-end
}
}