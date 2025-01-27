use vstd::prelude::*;

verus! {

fn is_sub_list_at_index(main: &Vec<i32>, sub: &Vec<i32>, idx: usize) -> (result: bool)
    // pre-conditions-start
    requires
        sub.len() <= main.len(),
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
            0 <= idx + i <= main.len(),
            forall|k: int| 0 <= k < i ==> main[idx + k] == sub[k],
            forall|k: int|
                0 <= k < i ==> (main@.subrange(idx as int, (idx + k)) =~= sub@.subrange(0, k)),
        // invariants-end
    {
        if (main[idx + i] != sub[i]) {
            // assert-start
            assert(exists|k: int| 0 <= k < i ==> main[idx + k] != sub[k]);
            assert(main@.subrange(idx as int, (idx + sub@.len())) != sub@);
            // assert-end
            return false;
        }
        i += 1;
    }
    // assert-start
    assert(main@.subrange(idx as int, (idx + sub@.len())) == sub@);
    // assert-end
    true
    // impl-end
}

fn is_sub_list(main: &Vec<i32>, sub: &Vec<i32>) -> (result: bool)
    // pre-conditions-start
    requires
        sub.len() <= main.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        result == (exists|k: int, l: int|
            0 <= k <= (main.len() - sub.len()) && l == k + sub.len() && (#[trigger] (main@.subrange(
                k,
                l,
            ))) =~= sub@),
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
            forall|k: int, l: int|
                (0 <= k < index) && l == k + sub.len() ==> (#[trigger] (main@.subrange(k, l))
                    != sub@),
        // invariants-end
    {
        if (is_sub_list_at_index(&main, &sub, index)) {
            return true;
        }
        index += 1;
    }
    false
    // impl-end
}

} // verus!

fn main() {}