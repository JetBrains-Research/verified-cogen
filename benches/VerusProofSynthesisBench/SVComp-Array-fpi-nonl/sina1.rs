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
		forall |k:int| 0 <= k < N ==> a[k] == N,
	// post-conditions-end
{
	// impl-start
	let mut i: usize = 0;
	sum.set(0, 0);

	while (i < N as usize)
		// invariants-start
		invariant
			i <= N,
			sum.len() == 1,
			sum[0] == i,
		// invariants-end
	{
		sum.set(0, sum[0] + 1);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			forall |k:int| 0 <= k < i ==> a[k] == sum[0],
			sum.len() == 1,
			a.len() == N,
		// invariants-end
	{
		a.set(i, sum[0]);
		i = i + 1;
	}
	// impl-end
}
}

fn main() {}