use vstd::prelude::*;

verus! {

spec fn three_distinct_spec(s: Seq<char>, i: int) -> bool
    recommends
        0 < i && i + 1 < s.len(),
{
    (s[i - 1] != s[i]) && (s[i] != s[i + 1]) && (s[i] != s[i + 1])
}

fn three_distinct(s: &Vec<char>, i: usize) -> (is: bool)
    requires
        0 < i && i + 1 < s.len(),
    ensures
        is <==> three_distinct_spec(s@, i as int),
{
    (s[i - 1] != s[i]) && (s[i] != s[i + 1]) && (s[i] != s[i + 1])
}

spec fn happy_spec(s: Seq<char>) -> bool {
    s.len() >= 3 && (forall|i: int| 0 < i && i + 1 < s.len() ==> three_distinct_spec(s, i))
}

#[verifier::loop_isolation(false)]
fn is_happy(s: &Vec<char>) -> (happy: bool)
    ensures
        happy <==> happy_spec(s@),
{
    if s.len() < 3 {
        return false;
    }
    for i in 1..(s.len() - 1)
        invariant
            forall|j: int| 0 < j < i ==> three_distinct_spec(s@, j),
    {
        if !three_distinct(s, i) {
            return false;
        }
    }
    return true;
}

} 
fn main() {}
