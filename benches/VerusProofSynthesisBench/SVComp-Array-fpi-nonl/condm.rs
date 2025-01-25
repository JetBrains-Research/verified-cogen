use vstd::prelude::*;
fn main() {}
verus!{
fn myfun(a: &mut Vec<i32>, N: u32)
	// pre-conditions-start
	requires
		N > 0,
		old(a).len() == N,
	// pre-conditions-end
	// post-conditions-start
	ensures
		forall |k:int| 0 <= k < N ==> a[k] % 2 == N % 2,
	// post-conditions-end
{
	// impl-start
	let mut i: usize = 0;

	while (i < N as usize)
		// invariants-start
		invariant
			forall |k:int| 0 <= k < i ==> a[k] == 0,
			a.len() == N,
		// invariants-end
	{
		a.set(i, 0);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			forall |k:int| 0 <= k < i ==> a[k] % 2 == N % 2,
			forall |k:int| i <= k < N ==> a[k] == 0,
			a.len() == N,
		// invariants-end
	{
		if (N % 2 == 0) {
			a.set(i, a[i] + 2);
		} else {
			a.set(i, a[i] + 1);
		}
		i = i + 1;
	}
	// impl-end
}
}