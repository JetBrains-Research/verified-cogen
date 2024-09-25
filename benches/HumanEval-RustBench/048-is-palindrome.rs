use vstd::prelude::*;

verus! {

fn is_palindrome(text: &str) -> (result: bool)
    ensures
        result == forall|i: int|
            0 <= i < text@.len() ==> #[trigger] text@[i] == text@[text@.len() - 1 - i],
{
    let text_len: usize = text.unicode_len();
    for pos in 0..text_len / 2
        invariant
            text_len == text@.len(),
            forall|i: int| 0 <= i < pos ==> #[trigger] text@[i] == text@[text_len - 1 - i],
    {
        if text.get_char(pos) != text.get_char(text_len - 1 - pos) {
            return false;
        }
    }
    true
}

} 
fn main() {}
