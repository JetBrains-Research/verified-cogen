use vstd::prelude::*;

verus!{
fn myfun(a: &mut Vec<i32>, sum: &mut Vec<i32>, N: i32)
	// pre-conditions-start
	requires
		N > 0,
		old(a).len() == N,
		old(sum).len() == 1,
	// pre-conditions-end
	// post-conditions-start
	ensures
		forall |k:int| 0 <= k < N ==> a[k] == 0,
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
			i <= N,
			forall |k:int| 0 <= k < N ==> a[k] == 1,
			a.len() == N,
			sum[0] == i,
			sum.len() == 1,
		// invariants-end
	{
		sum.set(0, sum[0] + a[i]);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			forall |k:int| 0 <= k < i ==> a[k] == 0,
			forall |k:int| i <= k < N ==> a[k] == 1,
			a.len() == N,
			sum.len() == 1,
			sum[0] == N,
		// invariants-end
	{
		if (sum[0] == N) {
			a.set(i, a[i] - 1);
		} else {
			a.set(i, a[i] + 1);
		}
		i = i + 1;
	}
	// impl-end
}
}

fn main() {}