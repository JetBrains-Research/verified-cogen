use vstd::prelude::*;

verus! {

spec fn abs_spec(i: int) -> int {
    if i < 0 { -i } else { i }
}

fn abs(i: i32) -> (res: i32)
    requires
        i != i32::MIN,
    ensures
        i < 0 ==> res == -i,
        i >= 0 ==> res == i
{
    if i < 0 { -i } else { i }
}

#[verifier::loop_isolation(false)]
fn has_close_elements(numbers: &[i32], threshold: i32) -> (flag: bool)
    // pre-conditions-start
    requires
        threshold > 0,
        forall|i: int, j: int| 0 <= i && i < numbers.len() && 0 <= j && j < numbers.len() ==> numbers[i] - numbers[j] < i32::MAX && -(numbers[i] - numbers[j]) < i32::MAX
    // pre-conditions-end
    // post-conditions-start
    ensures
        flag == exists|i: int, j: int| 0 <= i && 0 <= j && i < numbers.len() && j < numbers.len() && i != j && abs_spec(numbers[i] - numbers[j]) < threshold
    // post-conditions-end
{
    // impl-start
    let mut flag = false;
    let mut i = 0;
    while i < numbers.len()
        // invariants-start
        invariant
            0 <= i && i <= numbers.len(),
            flag == exists|i1: int, j1: int| 0 <= i1 && 0 <= j1 && i1 < i && j1 < numbers.len() && i1 != j1 && abs_spec(numbers[i1] - numbers[j1]) < threshold,
        // invariants-end
    {
        let mut j = 0;
        while j < numbers.len()
            // invariants-start
            invariant
                0 <= i && i < numbers.len(),
                0 <= j && j <= numbers.len(),
                flag == exists|i1: int, j1: int| 0 <= i1 && 0 <= j1 && ((i1 < i && j1 < numbers.len()) || (i1 == i && j1 < j)) && i1 != j1 && abs_spec(numbers[i1] - numbers[j1]) < threshold,
            // invariants-end
        {
            if i != j {
                let distance = abs(numbers[i] - numbers[j]);
                if distance < threshold {
                    flag = true;
                }
            }
            j = j + 1;
        }
        i = i + 1;
    }
    flag
    // impl-end
}

fn main() {}
}
