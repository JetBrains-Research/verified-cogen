use vstd::arithmetic::logarithm::log;
use vstd::arithmetic::power::pow;
use vstd::prelude::*;
verus! {
#[verifier::external_fn_specification]
fn ex_ilog(x: u32, base: u32) -> (ret: u32)
    requires
        x > 0,
        base > 1,
    ensures
        ret == log(base as int, x as int),
{
    // impl-start
    x.ilog(base)
    // impl-end
}

#[verifier::external_fn_specification]
fn ex_checked_pow(x: u32, exp: u32) -> (ret: Option<u32>)
    ensures
        ret.is_some() <==> ret.unwrap() == pow(x as int, exp as nat),
        ret.is_none() <==> pow(x as int, exp as nat) > u32::MAX,
{
    // impl-start
    x.checked_pow(exp)
    // impl-end
}

fn is_simple_power(x: u32, n: u32) -> (ret: bool)
    // pre-conditions-start
    requires
        x > 0,
        n > 1,
    // pre-conditions-end
    // post-conditions-start
    ensures
        ret <==> x == pow(n as int, log(n as int, x as int) as nat),
    // post-conditions-end
{
    // impl-start
    let maybe_x = n.checked_pow(x.ilog(n));
    return maybe_x.is_some() && maybe_x.unwrap() == x;
    // impl-end
}

}
fn main() {}
