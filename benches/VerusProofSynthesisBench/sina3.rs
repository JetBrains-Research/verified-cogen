use vstd::prelude::*;
fn main() {}
verus!{
fn myfun(a: &mut Vec<i32>, b: &mut Vec<i32>, sum: &mut Vec<i32>, N: i32)
	// pre-conditions-start
	requires
		N > 0,
		old(a).len() == N,
		old(b).len() == N,
		old(sum).len() == 1,
		N < 1000,
	// pre-conditions-end
	// post-conditions-start
	ensures
		forall |k:int| 0 <= k < N ==> a[k] == N + 1,
	// post-conditions-end
{
	// impl-start
	sum.set(0, 0);
	let mut i: usize = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			forall |k:int| 0 <= k < i ==> a[k] == 1,
			a.len() == N,
		// invariants-end
	{
		a.set(i, 1);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			forall |k:int| 0 <= k < i ==> b[k] == 1,
			b.len() == N,
		// invariants-end
	{
		b.set(i, 1);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			i <= N,
			sum.len() == 1,
			forall |k:int| 0 <= k < N ==> a[k] == 1,
			a.len() == N,
			sum[0] == i,
		// invariants-end
	{
		sum.set(0, sum[0] + a[i]);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			forall |k:int| 0 <= k < N ==> b[k] == 1,
			forall |k:int| 0 <= k < i ==> a[k] == N + 1,
			a.len() == N,
			b.len() == N,
			sum.len() == 1,
			sum[0] == N,
			N < 1000,
		// invariants-end
	{
		a.set(i, b[i] + sum[0]);
		i = i + 1;
	}
	// impl-end
}
}