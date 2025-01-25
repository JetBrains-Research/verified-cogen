use vstd::prelude::*;
fn main() {}
verus!{
fn myfun(a: &mut Vec<i32>, sum: &mut Vec<i32>, N: usize)
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
	while (i < N)
		// invariants-start
		invariant
			a.len() == N,
			forall |k:int| 0<= k < i ==> a[k] == 1,
		// invariants-end
	{
		a.set(i, 1);
		i = i + 1;
	}

	i = 0;
	while (i < N)
		// invariants-start
		invariant
			a.len() == N,
			forall |k:int| 0<= k < i ==> a[k] == 2,
			forall |k:int| i<= k < N ==> a[k] == 1,
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
	while (i < N)
		// invariants-start
		invariant
			i <= N,
			a.len() == N,
			forall |k:int| 0<= k < N ==> a[k] == 2,
			sum.len() == 1,
			sum[0] == 2 * i,
			N < 1000,
		// invariants-end
	{
		if (a[i] == 2) {
			sum.set(0, sum[0] + a[i]);
		} else {
			sum.set(0, sum[0] * a[i]);
		}
		i = i + 1;
	}
	// impl-end
}
}