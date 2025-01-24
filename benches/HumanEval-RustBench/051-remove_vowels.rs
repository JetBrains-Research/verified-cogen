use vstd::prelude::*;

verus! {

spec fn is_vowel_spec(c: char) -> (result:bool) {
    c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' || c == 'A' || c == 'E' || c == 'I'
        || c == 'O' || c == 'U'
}
// pure-end

fn is_vowel(c: char) -> (is_vowel: bool)
    // post-conditions-start
    ensures
        is_vowel == is_vowel_spec(c),
    // post-conditions-end
{
    // impl-start
    c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' || c == 'A' || c == 'E' || c == 'I'
        || c == 'O' || c == 'U'
    // impl-end
}

fn remove_vowels(str: &[char]) -> (str_without_vowels: Vec<char>)
    // post-conditions-start
    ensures
        str_without_vowels@ == str@.filter(|x: char| !is_vowel_spec(x)),
    // post-conditions-end
{
    // impl-start
    let ghost str_length = str.len();
    let mut str_without_vowels: Vec<char> = Vec::new();
    // assert-start
    assert(str@.take(0int).filter(|x: char| !is_vowel_spec(x)) == Seq::<char>::empty());
    // assert-end

    for index in 0..str.len()
        // invariants-start
        invariant
            str_without_vowels@ == str@.take(index as int).filter(|x: char| !is_vowel_spec(x)),
        // invariants-end
    {
        if !is_vowel(str[index]) {
            str_without_vowels.push(str[index]);
        }
        // assert-start
        assert(str@.take((index + 1) as int).drop_last() == str@.take(index as int));
        // assert-end
        reveal(Seq::filter);
    }
    // assert-start
    assert(str@ == str@.take(str_length as int));
    // assert-end
    str_without_vowels
    // impl-end
}

} // verus!
fn main() {}
