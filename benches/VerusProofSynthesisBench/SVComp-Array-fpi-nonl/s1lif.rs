use vstd::prelude::*;
fn main() {}
verus!{
fn myfun(a: &mut Vec<i32>, sum: &mut Vec<i32>, N: i32)
	// pre-conditions-start
	requires
		N > 0,
		old(a).len() == N,
		old(sum).len() == 1,
		N < 1000,
	// pre-conditions-end
	// post-conditions-start
	ensures
		sum[0] == 2 * N,
	// post-conditions-end
{
	// impl-start
	sum.set(0, 0);
	let mut i: usize = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			a.len() == N,
			forall |j: int| 0<= j < i ==> a[j] == 1,
		// invariants-end
	{
		a.set(i, 1);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			a.len() == N,
			forall |j: int| 0<= j < i ==> a[j] == 2,
			forall |j: int| i<= j < N ==> a[j] == 1,
		// invariants-end
	{
		if (a[i] == 1) {
			a.set(i, a[i] + 1);
		} else {
			a.set(i, a[i] - 1);
		}
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			i <= N,
			a.len() == N,
			forall |j: int| 0<= j < N ==> a[j] == 2,
			sum.len() == 1,
			sum[0] == 2 * i,
			N < 1000,
		// invariants-end
	{
		sum.set(0, sum[0] + a[i]);
		i = i + 1;
	}
	// impl-end
}
}