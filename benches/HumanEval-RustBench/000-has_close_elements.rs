use vstd::math::abs;
use vstd::prelude::*;
use vstd::slice::*;

verus! {
fn has_close_elements(numbers: &[i64], threshold: i64) -> (result: bool)
    ensures
        result == exists|i: int, j: int|
            0 <= i < j < numbers@.len() && abs(numbers[i] - numbers[j]) < threshold,
{
    if threshold <= 0 {
        assert(forall|i: int, j: int|
            0 <= i < j < numbers@.len() ==> abs(numbers[i] - numbers[j]) >= 0 >= threshold);
        return false;
    }
    let max_minus_threshold: i64 = i64::MAX - threshold;
    let numbers_len: usize = numbers.len();
    for x in 0..numbers_len
        invariant
            max_minus_threshold == i64::MAX - threshold,
            numbers_len == numbers@.len(),
            forall|i: int, j: int|
                0 <= i < j < numbers@.len() && i < x ==> abs(numbers[i] - numbers[j]) >= threshold,
    {
        let numbers_x: i64 = *slice_index_get(numbers, x);  
        for y in x + 1..numbers_len
            invariant
                max_minus_threshold == i64::MAX - threshold,
                numbers_len == numbers@.len(),
                x < numbers@.len(),
                numbers_x == numbers[x as int],
                forall|i: int, j: int|
                    0 <= i < j < numbers@.len() && i < x ==> abs(numbers[i] - numbers[j])
                        >= threshold,
                forall|j: int| x < j < y ==> abs(numbers_x - numbers[j]) >= threshold,
        {
            let numbers_y = *slice_index_get(numbers, y);  
            if numbers_x > numbers_y {
                if numbers_y > max_minus_threshold {
                    return true;
                }
                if numbers_x < numbers_y + threshold {
                    return true;
                }
            } else {
                if numbers_x > max_minus_threshold {
                    return true;
                }
                if numbers_y < numbers_x + threshold {
                    return true;
                }
            }
        }
    }
    false
}

} 
fn main() {}
