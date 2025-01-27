use vstd::prelude::*;

verus! {

spec fn expr_inner_longest(strings: &Vec<Vec<u8>>, result: Option<&Vec<u8>>) -> (result: bool) {
    match result {
        None => strings.len() == 0,
        Some(s) => {
            (forall|i: int| #![auto] 0 <= i < strings.len() ==> s.len() >= strings[i].len())
                && (exists|i: int|
                #![auto]
                (0 <= i < strings.len() && s == strings[i] && (forall|j: int|
                    #![auto]
                    0 <= j < i ==> strings[j].len() < s.len())))
        },
    }
}
// pure-end

fn longest(strings: &Vec<Vec<u8>>) -> (result: Option<&Vec<u8>>)
    // post-conditions-start
    ensures
        expr_inner_longest(strings, result),
    // post-conditions-end
{
    // impl-start
    if strings.len() == 0 {
        return None;
    }
    let mut result: &Vec<u8> = &strings[0];
    let mut pos = 0;

    for i in 1..strings.len()
        // invariants-start
        invariant
            0 <= pos < i,
            result == &strings[pos as int],
            exists|i: int| 0 <= i < strings.len() && strings[i] == result,
            forall|j: int| #![auto] 0 <= j < i ==> strings[j].len() <= result.len(),
            forall|j: int| #![auto] 0 <= j < pos ==> strings[j].len() < result.len(),
        // invariants-end
    {
        if result.len() < strings[i].len() {
            result = &strings[i];
            pos = i;
        }
    }
    Some(result)
    // impl-end
}

}
fn main() {}
