use vstd::prelude::*;

verus! {

spec fn encode_char_spec(c: int) -> (result:int)
    recommends
        65 <= c <= 90,
{
    (c - 65 + 5) % 26 + 65
}
// pure-end

fn encode_char(c: u8) -> (r: u8)
    // pre-conditions-start
    requires
        65 <= c <= 90,
    // pre-conditions-end
    // post-conditions-start
    ensures
        r == encode_char_spec(c as int),
        65 <= r <= 90,
    // post-conditions-end
{
    (c - 65 + 5) % 26 + 65
}

spec fn decode_char_spec(c: int) -> (result:int)
    recommends
        65 <= c <= 90,
{
    (c - 65 + 26 - 5) % 26 + 65
}
// pure-end

fn decode_char(c: u8) -> (r: u8)
    // pre-conditions-start
    requires
        65 <= c <= 90,
    // pre-conditions-end
    // post-conditions-start
    ensures
        r == decode_char_spec(c as int),
        65 <= r <= 90,
    // post-conditions-end
{
    // impl-start
    (c - 65 + 26 - 5) % 26 + 65
    // impl-end
}

proof fn opposite_encode_decode(c: int)
    // pre-conditions-start
    requires
        65 <= c <= 90,
    // pre-conditions-end
    // post-conditions-start
    ensures
        encode_char_spec(decode_char_spec(c)) == c,
        decode_char_spec(encode_char_spec(c)) == c,
    // post-conditions-end
{
}
// pure-end

#[verifier::loop_isolation(false)]
fn encode_shift(s: &Vec<u8>) -> (t: Vec<u8>)
    // pre-conditions-start
    requires
        forall|i: int| #![trigger s[i]] 0 <= i < s.len() ==> 65 <= s[i] <= 90,
    // pre-conditions-end
    // post-conditions-start
    ensures
        s.len() == t.len(),
        forall|i: int| #![auto] 0 <= i < t.len() ==> t[i] == encode_char_spec(s[i] as int),
        forall|i: int| #![auto] 0 <= i < t.len() ==> decode_char_spec(t[i] as int) == s[i],
    // post-conditions-end
{
    // impl-start
    let mut t: Vec<u8> = vec![];
    for i in 0..s.len()
        // invariants-start
        invariant
            t.len() == i,
            forall|j: int| #![auto] 0 <= j < i ==> t[j] == encode_char_spec(s[j] as int),
            forall|j: int| #![auto] 0 <= j < i ==> decode_char_spec(t[j] as int) == s[j],
        // invariants-end
    {
        t.push(encode_char(s[i]));
        // assert-start
        proof {
            opposite_encode_decode(s[i as int] as int);
        }
        // assert-end
    }
    t
    // impl-end
}

#[verifier::loop_isolation(false)]
fn decode_shift(s: &Vec<u8>) -> (t: Vec<u8>)
    // pre-conditions-start
    requires
        forall|i: int| #![trigger s[i]] 0 <= i < s.len() ==> 65 <= s[i] <= 90,
    // pre-conditions-end
    // post-conditions-start
    ensures
        s.len() == t.len(),
        forall|i: int| #![auto] 0 <= i < t.len() ==> t[i] == decode_char_spec(s[i] as int),
        forall|i: int| #![auto] 0 <= i < t.len() ==> encode_char_spec(t[i] as int) == s[i],
    // post-conditions-end
{
    // impl-start
    let mut t: Vec<u8> = vec![];
    for i in 0..s.len()
        // invariants-start
        invariant
            t.len() == i,
            forall|j: int| #![auto] 0 <= j < i ==> t[j] == decode_char_spec(s[j] as int),
            forall|j: int| #![auto] 0 <= j < i ==> encode_char_spec(t[j] as int) == s[j],
        // invariants-end
    {
        t.push(decode_char(s[i]));
        // assert-start
        proof {
            opposite_encode_decode(s[i as int] as int);
        }
        // assert-end
    }
    t
    // impl-end
}

}
fn main() {}
