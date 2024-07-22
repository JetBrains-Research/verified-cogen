#![crate_name = "transpose_matrix"]

use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn transpose(matrix: Vec<Vec<i32>>) -> (result: Vec<Vec<i32>>)
    requires
        matrix.len() > 0,
        forall|i: int| #![trigger matrix[i]]
            0 <= i < matrix.len() ==> matrix[i].len() == matrix[0].len(),
        forall|i: int| #![trigger matrix[i]]
            0 <= i < matrix.len() ==> matrix[i].len() == matrix.len()
    ensures
        result.len() == matrix[0].len(),
        forall|i: int| #![trigger result[i]]
            0 <= i < result.len() ==> result[i].len() == matrix.len(),
        forall|i: int, j: int| #![trigger result[i], matrix[j]]
            0 <= i < result.len() && 0 <= j < result[i].len() ==> result[i][j] == matrix[j][i]
{
    let n = matrix.len();
    assert(forall|i: int| #![trigger matrix[i]]
        0 <= i < n ==> matrix[i].len() == n);
    let mut result: Vec<Vec<i32>> = Vec::new();
    let mut i = 0;
    while i < matrix.len()
        invariant
            0 <= i <= matrix.len(),
            result.len() == i,
            forall|j: int| #![trigger result[j]]
                0 <= j < result.len() ==> result[j].len() == matrix.len(),
            forall|j: int, k: int| #![trigger result[j], matrix[k]]
                0 <= j < result.len() && 0 <= k < result[j].len() ==> result[j][k] == matrix[k][j],
    {
        let mut row = Vec::new();
        let mut j = 0;
        while j < matrix.len()
            invariant
                0 <= j <= matrix.len(),
                row.len() == j,
                forall|k: int| #![trigger result[k], matrix[k]]
                    0 <= k < j ==> row[k] == matrix[k][i as int],
        {
            row.push(matrix[j][i]);
            j += 1;
        }
        result.push(row);
    }
    result
}

fn main() {}
}
