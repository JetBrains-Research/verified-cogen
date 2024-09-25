use vstd::prelude::*;

verus! {

fn string_eq(s1: &str, s2: &str) -> (result: bool)
    ensures
        result <==> s1@ == s2@,
{
    let s1_len = s1.unicode_len();
    let s2_len = s2.unicode_len();
    if s1_len != s2_len {
        return false;
    }
    for i in 0..s1_len
        invariant
            s1@.subrange(0, i as int) =~= s2@.subrange(0, i as int),
            i <= s1_len == s2_len == s1@.len() == s2@.len(),
    {
        let c = s1.get_char(i);
        if c != s2.get_char(i) {
            return false;
        }
        assert(s1@.subrange(0, i + 1) == s1@.subrange(0, i as int).push(c));
        assert(s1@.subrange(0, i as int).push(c) == s2@.subrange(0, i as int).push(c));
        assert(s2@.subrange(0, i as int).push(c) == s2@.subrange(0, i + 1));
    }
    assert(s1@ == s1@.subrange(0, s1_len as int));
    assert(s2@ == s2@.subrange(0, s2_len as int));
    true
}

fn check_substring(s: &str, sub: &str) -> (result: bool)
    ensures
        result <==> exists|i: int|
            0 <= i <= s@.len() - sub@.len() && s@.subrange(i, #[trigger] (i + sub@.len())) == sub@,
{
    let s_len = s.unicode_len();
    let sub_len = sub.unicode_len();
    if (s_len < sub_len) {
        return false;
    }
    if sub_len == 0 {
        assert(s@.subrange(0, (0 + sub@.len()) as int) == sub@);
        return true;
    }
    for i in 0..s_len - sub_len + 1
        invariant
            forall|j: int| 0 <= j < i ==> s@.subrange(j, #[trigger] (j + sub@.len())) != sub@,
            i <= s_len - sub_len + 1,
            sub_len == sub@.len() <= s_len == s@.len(),
            sub_len > 0,
    {
        if string_eq(sub, s.substring_char(i, i + sub_len)) {
            assert(0 <= i <= s@.len() - sub@.len());
            assert(s@.subrange(i as int, i + sub@.len()) == sub@);
            return true;
        }
    }
    false
}

fn filter_by_substring<'a>(strings: &Vec<&'a str>, substring: &str) -> (res: Vec<&'a str>)
    ensures
        forall|i: int|
            0 <= i < strings@.len() && (exists|j: int|
                0 <= j <= strings@[i]@.len() - substring@.len() && strings[i]@.subrange(
                    j,
                    #[trigger] (j + substring@.len()),
                ) == substring@) ==> res@.contains(#[trigger] (strings[i])),
{
    let mut res = Vec::new();
    for n in 0..strings.len()
        invariant
            forall|i: int|
                0 <= i < n && (exists|j: int|
                    0 <= j <= strings@[i]@.len() - substring@.len() && strings[i]@.subrange(
                        j,
                        #[trigger] (j + substring@.len()),
                    ) == substring@) ==> res@.contains(#[trigger] (strings[i])),
    {
        if check_substring(strings[n], substring) {
            let ghost res_old = res;
            res.push(strings[n]);
            assert(res@.last() == strings[n as int]);
            assert(res@.drop_last() == res_old@);
        }
    }
    res
}

} 
fn main() {}
