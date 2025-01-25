use vstd::prelude::*;
fn main() {}
verus!{
fn myfun(a: &mut Vec<i32>, N: i32, m: i32)
	// pre-conditions-start
	requires
		N > 0,
		old(a).len() == N,
	// pre-conditions-end
	// post-conditions-start
	ensures
		forall |k:int| 0 <= k < N ==> a[k] <= N,
	// post-conditions-end
{
	// impl-start
	let mut i: usize = 0;

	while (i < N as usize)
		// invariants-start
		invariant
			a.len() == N,
		// invariants-end
	{
		a.set(i, m);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			forall |k:int| 0 <= k < i ==> a[k] <= N,
			a.len() == N,
		// invariants-end
	{
		if (a[i] < N) {
			a.set(i, a[i]);
		} else {
			a.set(i, N);
		}
		i = i + 1;
	}
	// impl-end
}
}