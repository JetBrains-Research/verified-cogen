use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn string_xor(a: &[char], b: &[char]) -> (result: Vec<char>)
    requires
        a.len() == b.len(),
        forall|i: int| 0 <= i && i < a.len() ==> a[i] == '0' || a[i] == '1',
        forall|i: int| 0 <= i && i < b.len() ==> b[i] == '0' || b[i] == '1',
    ensures
        result.len() == a.len(),
        forall|i: int| 0 <= i && i < result.len() ==> (result[i] == '0' || result[i] == '1'),
        forall|i: int| 0 <= i && i < result.len() ==> result[i] == (if a[i] == b[i] { '0' } else { '1' })
{
    let mut result: Vec<char> = Vec::new();
    let mut i = 0;
    while i < a.len()
    {
        let bit = if a[i] == b[i] { '0' } else { '1' };
        result.push(bit);
        i += 1;
    }
    result
}

fn main() {}
}
