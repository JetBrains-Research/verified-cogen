use vstd::prelude::*;

verus! {

fn sub_array_at_index(main: &Vec<i32>, sub: &Vec<i32>, idx: usize) -> (result: bool)
    // pre-conditions-start
    requires
        0 <= idx <= (main.len() - sub.len()),
    // pre-conditions-end
    // post-conditions-start
    ensures
        result == (main@.subrange(idx as int, (idx + sub@.len())) =~= sub@),
    // post-conditions-end
{
    // impl-start
    let mut i = 0;
    while i < sub.len()
        // invariants-start
        invariant
            0 <= idx <= (main.len() - sub.len()),
            0 <= i <= sub.len(),
            forall|k: int| 0 <= k < i ==> main[idx + k] == sub[k],
        // invariants-end
    {
        if (main[idx + i] != sub[i]) {
            return false;
        }
        i += 1;
    }
    true
    // impl-end
}

spec fn is_subrange_at(main: Seq<i32>, sub: Seq<i32>, i: int) -> (result: bool) {
    sub =~= main.subrange(i, i+sub.len())
}
// pure-end

fn is_sub_array(main: &Vec<i32>, sub: &Vec<i32>) -> (result: bool)
    // post-conditions-start
    ensures
        result == (exists|k: int|
            0 <= k <= (main.len() - sub.len()) && is_subrange_at(main@, sub@, k)),
    // post-conditions-end
{
    // impl-start
    if sub.len() > main.len() {
        return false;
    }
    let mut index = 0;
    while index <= (main.len() - sub.len())
        // invariants-start
        invariant
            sub.len() <= main.len(),
            0 <= index <= (main.len() - sub.len()) + 1,
            forall |k:int| 0<= k < index ==> !is_subrange_at(main@, sub@, k),
        // invariants-end
    {
        if (sub_array_at_index(&main, &sub, index)) {
            // assert-start
            assert(is_subrange_at(main@, sub@, index as int));
            // assert-end
            return true;
        }
        index += 1;
    }
    false
    // impl-end
}

} // verus!

fn main() { }
