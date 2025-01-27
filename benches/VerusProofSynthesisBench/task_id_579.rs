use vstd::prelude::*;

verus! {

proof fn lemma_vec_push<T>(vec: Seq<T>, i: T, l: usize)
    // pre-conditions-start
    requires
        l == vec.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        forall|k: int| 0 <= k < vec.len() ==> #[trigger] vec[k] == vec.push(i)[k],
        vec.push(i).index(l as int) == i,
    // post-conditions-end
{
    // impl-start
    // impl-end
}
// pure-end

fn contains(arr: &Vec<i32>, key: i32) -> (result: bool)
    // post-conditions-start
    ensures
        result == (exists|i: int| 0 <= i < arr.len() && (arr[i] == key)),
    // post-conditions-end
{
    // impl-start
    let mut index = 0;
    while index < arr.len()
        // invariants-start
        invariant
            forall|m: int| 0 <= m < index ==> (arr[m] != key),
        // invariants-end
    {
        if (arr[index] == key) {
            return true;
        }
        index += 1;
    }
    false
    // impl-end
}

fn find_dissimilar(arr1: &Vec<i32>, arr2: &Vec<i32>) -> (result: Vec<i32>)
    // post-conditions-start
    ensures
        forall|i: int|
            0 <= i < arr1.len() ==> (!arr2@.contains(#[trigger] arr1[i]) ==> result@.contains(
                arr1[i],
            )),
        forall|i: int|
            0 <= i < arr2.len() ==> (!arr1@.contains(#[trigger] arr2[i]) ==> result@.contains(
                arr2[i],
            )),
        forall|i: int, j: int|
            0 <= i < j < result.len() ==> #[trigger] result[i] != #[trigger] result[j],
    // post-conditions-end
{
    // impl-start
    let mut result = Vec::new();
    let ghost mut output_len: int = 0;

    let mut index = 0;
    while index < arr1.len()
        // invariants-start
        invariant
            forall|i: int|
                0 <= i < index ==> (!arr2@.contains(#[trigger] arr1[i]) ==> result@.contains(
                    arr1[i],
                )),
            forall|m: int, n: int|
                0 <= m < n < result.len() ==> #[trigger] result[m] != #[trigger] result[n],
        // invariants-end
    {
        if (!contains(arr2, arr1[index]) && !contains(&result, arr1[index])) {
            // assert-start
            proof {
                lemma_vec_push(result@, arr1[index as int], result.len());
                output_len = output_len + 1;
            }
            // assert-end
            result.push(arr1[index]);

        }
        index += 1;
    }
    let mut index = 0;
    while index < arr2.len()
        // invariants-start
        invariant
            forall|i: int|
                0 <= i < arr1.len() ==> (!arr2@.contains(#[trigger] arr1[i]) ==> result@.contains(
                    arr1[i],
                )),
            forall|i: int|
                0 <= i < index ==> (!arr1@.contains(#[trigger] arr2[i]) ==> result@.contains(
                    arr2[i],
                )),
            forall|m: int, n: int|
                0 <= m < n < result.len() ==> #[trigger] result[m] != #[trigger] result[n],
        // invariants-end
    {
        if (!contains(arr1, arr2[index]) && !contains(&result, arr2[index])) {
            // assert-start
            proof {
                lemma_vec_push(result@, arr2[index as int], result.len());
                output_len = output_len + 1;
            }
            // assert-end
            result.push(arr2[index]);
        }
        index += 1;
    }
    // assert-start
    assert(forall|i: int|
        0 <= i < arr1.len() ==> (!arr2@.contains(#[trigger] arr1[i]) ==> result@.contains(
            arr1[i],
        )));
    assert(forall|i: int|
        0 <= i < arr2.len() ==> (!arr1@.contains(#[trigger] arr2[i]) ==> result@.contains(
            arr2[i],
        )));
    assert(forall|i: int, j: int|
        0 <= i < j < result.len() ==> #[trigger] result[i] != #[trigger] result[j]);
    // assert-end

    result
    // impl-end
}

} // verus!

fn main() {}
