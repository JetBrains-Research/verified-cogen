use vstd::prelude::*;

verus! {

fn intersperse(numbers: &[i32], delim: i32) -> (res: Vec<i32>)
    ensures
        numbers.len() == 0 ==> res.len() == 0,
        numbers.len() != 0 ==> res.len() == 2 * numbers.len() - 1,
        forall|i: int| 0 <= i && i < res.len() && i % 2 == 0 ==> res[i] == numbers[i / 2],
        forall|i: int| 0 <= i && i < res.len() && i % 2 == 1 ==> res[i] == delim
{
    let mut res = Vec::new();
    if numbers.len() != 0 {
        let mut i = 0;
        while i + 1 < numbers.len()
            invariant
                0 <= i && i < numbers.len(),
                res.len() == 2 * i,
                forall|j: int| 0 <= j && j < res.len() && j % 2 == 0 ==> res[j] == numbers[j / 2],
                forall|j: int| 0 <= j && j < res.len() && j % 2 == 1 ==> res[j] == delim
        {
            res.push(numbers[i]);
            res.push(delim);
            i += 1;
        }
        res.push(numbers[i]);
    }
    res
}

fn main() {}
}
