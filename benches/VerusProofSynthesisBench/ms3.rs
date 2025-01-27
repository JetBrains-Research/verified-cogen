use vstd::prelude::*;
fn main() {}
verus!{

fn myfun(a: &mut Vec<i32>, sum: &mut Vec<i32>, N: i32) 
	// pre-conditions-start
	requires 
		old(a).len() == N,
		old(sum).len() == 1,
		N > 0,
		N < 1000,
	// pre-conditions-end
	// post-conditions-start
	ensures
		sum[0] <= 2 * N,
	// post-conditions-end
{
	// impl-start
	let mut i: usize = 0;
	while (i < N as usize)
		// invariants-start
		invariant
			forall |k:int| 0<= k < i ==> a[k] == 0 || a[k] == 1 || a[k] == 2,
			a.len() == N,
		// invariants-end
	{
		a.set(i, (i % 3) as i32);
		i = i + 1;
	}

	i = 0;
	
	while (i < N as usize)
		// invariants-start
		invariant
			i <= N,
			forall |k:int| 0<= k < N ==> a[k] == 0 || a[k] == 1 || a[k] == 2,
			a.len() == N,
			sum.len() == 1,
			i > 0 ==> sum[0] <= 2 * i,
			N < 1000,
		// invariants-end
	{
		if (i == 0) {
			sum.set(0, 0);
		} else {
			sum.set(0, sum[0] + a[i]);
		}
		i = i + 1;
	}
	// impl-end
}
}