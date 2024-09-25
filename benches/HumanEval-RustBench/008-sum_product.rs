use vstd::prelude::*;

verus! {
pub open spec fn sum(numbers: Seq<u32>) -> int {
    numbers.fold_left(0, |acc: int, x| acc + x)
}
pub open spec fn product(numbers: Seq<u32>) -> int {
    numbers.fold_left(1, |acc: int, x| acc * x)
}
proof fn sum_bound(numbers: Seq<u32>)
    ensures
        sum(numbers) <= numbers.len() * u32::MAX,
    decreases numbers.len(),
{
    if numbers.len() == 0 {
    } else {
        sum_bound(numbers.drop_last());
    }
}
fn sum_product(numbers: Vec<u32>) -> (result: (u64, Option<u32>))
    requires
        numbers.len() < u32::MAX,
    ensures
        result.0 == sum(numbers@),
        result.1 matches Some(v) ==> v == product(numbers@),
{
    let mut sum_value: u64 = 0;
    let mut prod_value: Option<u32> = Some(1);
    for index in 0..numbers.len()
        invariant
            numbers.len() < u32::MAX,
            sum_value == sum(numbers@.take(index as int)),
            prod_value matches Some(v) ==> v == product(numbers@.take(index as int)),
            index <= numbers.len(),
            index >= 0,
    {
        proof {
            sum_bound(numbers@.take(index as int));
            assert(sum_value <= index * u32::MAX);
        }
        assert(numbers@.take(index as int + 1).drop_last() =~= numbers@.take(index as int));
        assert(numbers[index as int] == numbers@.take(index as int + 1).last());
        sum_value += numbers[index] as u64;
        prod_value =
        match prod_value {
            Some(v) => v.checked_mul(numbers[index]),
            None => None,
        };
    }
    assert(numbers@.take(numbers@.len() as int) =~= numbers@);
    (sum_value, prod_value)
}

} 
fn main() {}
