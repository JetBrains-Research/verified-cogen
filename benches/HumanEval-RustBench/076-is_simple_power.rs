use vstd::arithmetic::logarithm::log;
use vstd::arithmetic::power::pow;
use vstd::prelude::*;
verus! {
#[verifier::external_fn_specification]
pub fn ex_ilog(x: u32, base: u32) -> (ret: u32)
    requires
        x > 0,
        base > 1,
    ensures
        ret == log(base as int, x as int),
{
    x.ilog(base)
}

#[verifier::external_fn_specification]
pub fn ex_checked_pow(x: u32, exp: u32) -> (ret: Option<u32>)
    ensures
        ret.is_some() <==> ret.unwrap() == pow(x as int, exp as nat),
        ret.is_none() <==> pow(x as int, exp as nat) > u32::MAX,
{
    x.checked_pow(exp)
}

fn is_simple_power(x: u32, n: u32) -> (ret: bool)
    requires
        x > 0,
        n > 1,
    ensures
        ret <==> x == pow(n as int, log(n as int, x as int) as nat),
{
    let maybe_x = n.checked_pow(x.ilog(n));
    return maybe_x.is_some() && maybe_x.unwrap() == x;
}

} 
fn main() {}
