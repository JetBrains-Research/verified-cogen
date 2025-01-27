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
		sum[0] <= 2 * N,
	// post-conditions-end
{
	// impl-start
	sum.set(0, 0);
	let mut i: usize = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			a.len() == N,
			forall |k:int| 0 <= k < i ==> a[k] == 1,
		// invariants-end
	{
		a.set(i, 1);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			i <= N as usize,
			sum.len() == 1,
			a.len() == N,
			sum[0] == i, // Corrected invariant
			forall |k:int| 0 <= k < N ==> a[k] == 1,
		// invariants-end
	{
		sum.set(0, sum[0] + a[i]);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			b.len() == N,
			forall |k:int| 0 <= k < i ==> b[k] == 1,
		// invariants-end
	{
		b.set(i, 1);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			i <= N as usize,
			sum.len() == 1,
			b.len() == N,
			sum[0] == N + i,
			forall |k:int| 0 <= k < N ==> b[k] == 1,
			N < 1000,
		// invariants-end
	{
		sum.set(0, sum[0] + b[i]);
		i = i + 1;
	}
	// impl-end
}
}