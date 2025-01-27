use vstd::prelude::*;

verus! {
spec fn nesting_level(input: Seq<char>) -> (result:int)
    decreases input.len(),
{
    if input.len() == 0 {
        0
    } else {
        let prev_nesting_level = nesting_level(input.drop_last());
        let c = input.last();
        if c == '(' {
            prev_nesting_level + 1
        } else if c == ')' {
            prev_nesting_level - 1
        } else {
            prev_nesting_level
        }
    }
}
// pure-end

spec fn is_paren_char(c: char) -> (result:bool) {
    c == '(' || c == ')'
}
// pure-end

spec fn is_balanced_group(input: Seq<char>) -> (result:bool) {
    &&& input.len() > 0
    &&& nesting_level(input) == 0
    &&& forall|i| 0 <= i < input.len() ==> is_paren_char(#[trigger] input[i])
    &&& forall|i| 0 < i < input.len() ==> nesting_level(#[trigger] input.take(i)) > 0
}
// pure-end

spec fn is_sequence_of_balanced_groups(input: Seq<char>) -> (result:bool) {
    &&& nesting_level(input) == 0
    &&& forall|i| 0 < i < input.len() ==> nesting_level(#[trigger] input.take(i)) >= 0
}
// pure-end

spec fn vecs_to_seqs<T>(s: Seq<Vec<T>>) -> (result:Seq<Seq<T>>) {
    s.map(|_i, ss: Vec<T>| ss@)
}
// pure-end

spec fn remove_nonparens(s: Seq<char>) -> (result:Seq<char>) {
    s.filter(|c| is_paren_char(c))
}
// pure-end

proof fn lemma_remove_nonparens_maintained_by_push(s: Seq<char>, pos: int)
    // pre-conditions-start
    requires
        0 <= pos < s.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        ({
            let s1 = remove_nonparens(s.take(pos as int));
            let s2 = remove_nonparens(s.take((pos + 1) as int));
            if is_paren_char(s[pos]) {
                s2 == s1.push(s[pos])
            } else {
                s2 == s1
            }
        }),
    decreases pos,
    // post-conditions-end
{
    // impl-start
    reveal(Seq::filter);
    assert(s.take((pos + 1) as int).drop_last() =~= s.take(pos as int));
    if pos != 0 {
        lemma_remove_nonparens_maintained_by_push(s, pos - 1);
    }
    // impl-end
}
// pure-end

fn separate_paren_groups(input: &Vec<char>) -> (groups: Vec<Vec<char>>)
    // pre-conditions-start
    requires
        is_sequence_of_balanced_groups(input@),
    // pre-conditions-end
    // post-conditions-start
    ensures
        forall|i: int|
            #![trigger groups[i]]
            0 <= i < groups.len() ==> is_balanced_group(groups[i]@),
        vecs_to_seqs(groups@).flatten() == remove_nonparens(input@),
    // post-conditions-end
{
    // impl-start
    let mut groups: Vec<Vec<char>> = Vec::new();
    let mut current_group: Vec<char> = Vec::new();
    let input_len = input.len();
    let ghost mut ghost_groups: Seq<Seq<char>> = Seq::empty();
    // assert-start
    proof {
        assert(vecs_to_seqs(groups@) =~= ghost_groups);
        assert(remove_nonparens(input@.take(0)) =~= Seq::<char>::empty());
        assert(ghost_groups.flatten() + current_group@ =~= Seq::<char>::empty());
    }
    // assert-end
    let mut current_nesting_level: usize = 0;
    for pos in 0..input_len
        // invariants-start
        invariant
            input_len == input.len(),
            ghost_groups == vecs_to_seqs(groups@),
            ghost_groups.flatten() + current_group@ == remove_nonparens(input@.take(pos as int)),
            forall|i: int|
                #![trigger groups[i]]
                0 <= i < ghost_groups.len() ==> is_balanced_group(ghost_groups[i]),
            current_nesting_level == nesting_level(input@.take(pos as int)),
            current_nesting_level == nesting_level(current_group@),
            current_nesting_level <= pos,
            current_group@.len() == 0 <==> current_nesting_level == 0,
            forall|i| 0 <= i < current_group@.len() ==> is_paren_char(#[trigger] current_group@[i]),
            forall|i|
                0 < i < current_group@.len() ==> nesting_level(#[trigger] current_group@.take(i))
                    > 0,
            is_sequence_of_balanced_groups(input@),
        // invariants-end
    {
        let ghost prev_group = current_group@;
        let ghost prev_groups = ghost_groups;
        let c = input[pos];
        // assert-start
        proof {
            assert(input@.take((pos + 1) as int) == input@.take(pos as int).push(c));
            assert(input@.take((pos + 1) as int).drop_last() == input@.take(pos as int));
            lemma_remove_nonparens_maintained_by_push(input@, pos as int);
        }
        // assert-end
        if c == '(' {
            current_nesting_level = current_nesting_level + 1;
            current_group.push('(');
            // assert-start
            assert(current_group@.drop_last() == prev_group);
            assert(ghost_groups.flatten() + current_group@ =~= (ghost_groups.flatten()
                + prev_group).push('('));
            assert(forall|i|
                0 < i < prev_group.len() ==> #[trigger] current_group@.take(i) == prev_group.take(
                    i,
                ));
            // assert-end
        } else if c == ')' {
            current_nesting_level = current_nesting_level - 1;
            current_group.push(')');
            // assert-start
            assert(current_group@.drop_last() == prev_group);
            assert(ghost_groups.flatten() + current_group@ =~= (ghost_groups.flatten()
                + prev_group).push(')'));
            assert(forall|i|
                0 < i < prev_group.len() ==> #[trigger] current_group@.take(i) == prev_group.take(
                    i,
                ));
            // assert-end
            if current_nesting_level == 0 {
                proof {
                    ghost_groups = ghost_groups.push(current_group@);
                    // assert-start
                    assert(vecs_to_seqs(groups@.push(current_group)) =~= vecs_to_seqs(groups@).push(
                        current_group@,
                    ));
                    assert(ghost_groups.drop_last() == prev_groups);
                    assert(ghost_groups.flatten() =~= prev_groups.flatten() + current_group@) by {
                        prev_groups.lemma_flatten_and_flatten_alt_are_equivalent();
                        ghost_groups.lemma_flatten_and_flatten_alt_are_equivalent();
                    }
                    // assert-end
                }
                groups.push(current_group);
                current_group = Vec::<char>::new();
                // assert-start
                assert(ghost_groups.flatten() + current_group@ =~= remove_nonparens(
                    input@.take((pos + 1) as int),
                ));
                // assert-end
            }
        }
    }
    assert(input@.take(input_len as int) =~= input@); // assert-line
    assert(ghost_groups.flatten() + current_group@ == ghost_groups.flatten()); // assert-line
    groups
    // impl-end
}

}
fn main() {}
