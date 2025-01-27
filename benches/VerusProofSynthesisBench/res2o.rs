use vstd::prelude::*;

verus!{
fn myfun(a: &mut Vec<i32>, b: &mut Vec<i32>, c: &mut Vec<i32>, sum: &mut Vec<i32>, N: i32)
	// pre-conditions-start
	requires
		N > 0,
		old(a).len() == N,
		old(b).len() == N,
		old(c).len() == N,
		old(sum).len() == 1,
		N < 1000,
	// pre-conditions-end
	// post-conditions-start
	ensures
		sum[0] <= 3 * N,
	// post-conditions-end
{
	// impl-start
	let mut i: usize = 0;
	sum.set(0, 0);

	while (i < N as usize)
		// invariants-start
		invariant
			forall |j: int| 0<= j < i ==> a[j] == 1,
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
			forall |j: int| 0<= j < i ==> b[j] == 1,
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
			forall |j: int| 0<= j < i ==> c[j] == 1,
			c.len() == N,
		// invariants-end
	{
		c.set(i, 1);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			i <= N,
			sum.len() == 1,
			sum[0] == i,
			forall |j: int| 0<= j < N ==> a[j] == 1,
			a.len() == N,
		// invariants-end
	{
		sum.set(0, sum[0] + a[i]);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			i <= N,
			sum.len() == 1,
			sum[0] == i + N,
			forall |j: int| 0<= j < N ==> b[j] == 1,
			b.len() == N,
			N < 1000,
		// invariants-end
	{
		sum.set(0, sum[0] + b[i]);
		i = i + 1;
	}

	i = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			i <= N,
			sum.len() == 1,
			sum[0] == i + 2 * N,
			forall |j: int| 0<= j < N ==> c[j] == 1,
			c.len() == N,
			N < 1000,
		// invariants-end
	{
		sum.set(0, sum[0] + c[i]);
		i = i + 1;
	}
	// impl-end
}
}

fn main() {}
