use vstd::prelude::*;

verus! {

fn strlen(string: &Vec<char>) -> (length: usize)
    ensures
        length
            == string.len(),  
{
    string.len()
}

} 
fn main() {}
