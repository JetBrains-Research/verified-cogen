use vstd::prelude::*;

verus! {
spec fn fibo(n: int) -> (result:nat)
    decreases n
{
    if n <= 0 { 0 } else if n == 1 { 1 }
    else { fibo(n - 2) + fibo(n - 1) }
}
// pure-end

spec fn fibo_fits_i32(n: int) -> (result:bool) {
    fibo(n) < 0x8000_0000
}
// pure-end

proof fn fibo_is_monotonic(i: int, j: int)
    // pre-conditions-start
    requires
        i <= j,
    // pre-conditions-end
    // post-conditions-start
    ensures
        fibo(i) <= fibo(j),
    decreases j - i
    // post-conditions-end
{
    // impl-start
    if i <= 0 {
    }
    else if  i < j {
        fibo_is_monotonic(i, j-1);
        assert(fibo(j) == fibo(j-1)+fibo(j-2));
    }
    // impl-end
}
// pure-end

fn fibonacci(n: usize) -> (ret: Vec<i32>)
    // pre-conditions-start
    requires
        fibo_fits_i32(n as int),
        n >= 2,
    // pre-conditions-end
    // post-conditions-start
    ensures
        forall |i: int| 2 <= i < n ==> #[trigger] ret@[i] ==  fibo(i), 
        ret@.len() == n,
    // post-conditions-end
{
    // impl-start
    let mut fib = Vec::new();
    fib.push(0);
    fib.push(1);
    let mut i = 2;
    
    while i < n
        // invariants-start
        invariant
            forall |k: int| 0 <= k < i ==> #[trigger] fib@[k] == fibo(k),
            fibo_fits_i32(n as int),
            2 <= i,
            fib@.len() == i, 
            i <= n,
        // invariants-end
    {
        // assert-start
        proof{
            fibo_is_monotonic(i as int, n as int);
        }
        // assert-end
        let next_fib = fib[i - 1] + fib[i - 2];
        fib.push(next_fib);
        i += 1;
    }
    fib
    // impl-end
}
}

fn main() {}
