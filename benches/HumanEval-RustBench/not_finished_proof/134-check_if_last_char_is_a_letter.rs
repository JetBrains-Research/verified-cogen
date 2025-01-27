use vstd::prelude::*;

verus! {

pub spec fn is_alphabetic(c: char) -> (result: bool);
// pure-end

#[verifier::external_fn_specification]
#[verifier::when_used_as_spec(is_alphabetic)]
fn ex_is_alphabetic(c: char) -> (result: bool)
    // post-conditions-start
    ensures
        result <==> (c.is_alphabetic()),
    // post-conditions-end
{
    // impl-start
    c.is_alphabetic()
    // impl-end
}

pub spec fn is_whitespace(c: char) -> (result: bool);
// pure-end

#[verifier::external_fn_specification]
#[verifier::when_used_as_spec(is_whitespace)]
fn ex_is_whitespace(c: char) -> (result: bool)
    // post-conditions-start
    ensures
        result <==> (c.is_whitespace()),
    // post-conditions-end
{
    // impl-start
    c.is_whitespace()
    // impl-end
}

fn check_if_last_char_is_a_letter(txt: &str) -> (result: bool)
    // post-conditions-start
    ensures
        result <==> (txt@.len() > 0 && txt@.last().is_alphabetic() && (txt@.len() == 1
            || txt@.index(txt@.len() - 2).is_whitespace())),
    // post-conditions-end
{
    // impl-start
    let len = txt.unicode_len();
    if len == 0 {
        return false;
    }
    txt.get_char(len - 1).is_alphabetic() && (len == 1 || txt.get_char(len - 2).is_whitespace())
    // impl-end
}

}
fn main() {}