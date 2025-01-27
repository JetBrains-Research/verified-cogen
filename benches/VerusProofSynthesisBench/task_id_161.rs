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

fn contains(str: &Vec<i32>, key: i32) -> (result: bool)
    // post-conditions-start
    ensures
        result <==> (exists|i: int| 0 <= i < str.len() && (str[i] == key)),
    // post-conditions-end
{
    // impl-start
    let mut i = 0;
    while i < str.len()
        // invariants-start
        invariant
            forall|m: int| 0 <= m < i ==> (str[m] != key),
        // invariants-end
    {
        if (str[i] == key) {
            return true;
        }
        i += 1;
    }
    false
    // impl-end
}

fn remove_elements(arr1: &Vec<i32>, arr2: &Vec<i32>) -> (result: Vec<i32>)
    // post-conditions-start
    ensures
        forall|i: int|
            0 <= i < result.len() ==> (arr1@.contains(#[trigger] result[i]) && !arr2@.contains(
                #[trigger] result[i],
            )),
        forall|i: int|
            0 <= i < arr1.len() ==> (arr2@.contains(#[trigger] arr1[i]) || result@.contains(
                #[trigger] arr1[i],
            )),
    // post-conditions-end
{
    // impl-start
    let mut output_str = Vec::new();
    let mut index: usize = 0;
    let ghost mut output_len: int = 0;

    while index < arr1.len()
        // invariants-start
        invariant
            forall|k: int|
                0 <= k < output_str.len() ==> (arr1@.contains(#[trigger] output_str[k])
                    && !arr2@.contains(#[trigger] output_str[k])),
            forall|k: int|
                0 <= k < index ==> (arr2@.contains(#[trigger] arr1[k]) || output_str@.contains(
                    #[trigger] arr1[k],
                )),
        // invariants-end
    {
        if (!contains(arr2, arr1[index])) {
            // assert-start
            proof {
                lemma_vec_push(output_str@, arr1[index as int], output_str.len());
                output_len = output_len + 1;
            }
            // assert-end
            output_str.push(arr1[index]);
        }
        index += 1;
    }
    output_str
    // impl-end
}

} // verus!

fn main() {}
