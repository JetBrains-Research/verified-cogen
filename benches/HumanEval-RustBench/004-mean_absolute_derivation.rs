use vstd::arithmetic::div_mod::{
    lemma_div_is_ordered, lemma_div_is_ordered_by_denominator, lemma_div_multiples_vanish,
    lemma_fundamental_div_mod, lemma_fundamental_div_mod_converse,
};
use vstd::arithmetic::mul::{
    lemma_mul_inequality, lemma_mul_is_distributive_add, lemma_mul_is_distributive_add_other_way,
    lemma_mul_unary_negation,
};
use vstd::prelude::*;

verus! {
pub open spec fn sum(numbers: Seq<int>) -> int {
    numbers.fold_left(0, |acc: int, x| acc + x)
}
pub open spec fn mean(values: Seq<int>) -> int
    recommends
        values.len() > 0,
{
    sum(values) / (values.len() as int)
}
pub open spec fn abs(n: int) -> int {
    if n >= 0 {
        n
    } else {
        -n
    }
}
pub open spec fn spec_mean_absolute_deviation(numbers: Seq<int>) -> int
    recommends
        numbers.len() > 0,
{
    let avg = mean(numbers);
    sum(numbers.map(|_index, n: int| abs(n - avg))) / (numbers.len() as int)
}
proof fn lemma_sum_bound(numbers: Seq<int>, min: int, max: int)
    // pre-conditions-start
    requires
        forall|i| 0 <= i < numbers.len() ==> min <= #[trigger] numbers[i] <= max,
    // pre-conditions-end
    // post-conditions-start
    ensures
        numbers.len() * min <= sum(numbers) <= numbers.len() * max,
    // post-conditions-end
    decreases numbers.len(),
{
    // impl-start
    if numbers.len() != 0 {
        lemma_sum_bound(numbers.drop_last(), min, max);
        lemma_mul_is_distributive_add_other_way(min, numbers.len() - 1, 1);
        lemma_mul_is_distributive_add_other_way(max, numbers.len() - 1, 1);
    }
    // impl-end
}
proof fn lemma_sum_ratio_bound(numbers: Seq<int>, denominator: int, min: int, max: int)
    // pre-conditions-start
    requires
        forall|i| 0 <= i < numbers.len() ==> min <= #[trigger] numbers[i] <= max,
        denominator >= numbers.len(),
        denominator > 0,
        min <= 0,
        max >= 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        min <= sum(numbers) / denominator <= max,
    // post-conditions-end
{
    // impl-start
    lemma_sum_bound(numbers, min, max);
    // assert-start
    assert(denominator * min <= numbers.len() * min) by {
        lemma_mul_unary_negation(denominator, -min);
        lemma_mul_unary_negation(numbers.len() as int, -min);
        lemma_mul_inequality(numbers.len() as int, denominator, -min);
    }
    // assert-end
    // assert-start
    assert(numbers.len() * max <= denominator * max) by {
        lemma_mul_inequality(numbers.len() as int, denominator, max);
    }
    // assert-end
    lemma_div_multiples_vanish(min, denominator);
    lemma_div_multiples_vanish(max, denominator);
    lemma_div_is_ordered(denominator * min, sum(numbers), denominator);
    lemma_div_is_ordered(sum(numbers), denominator * max, denominator);
    // impl-end
}
proof fn lemma_how_to_update_running_sum(s: Seq<int>, i: int)
    // pre-conditions-start
    requires
        0 <= i < s.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        sum(s.take(i + 1)) == sum(s.take(i)) + s[i],
    // post-conditions-end
{
    // impl-start
    let q1 = s.take(i);
    let q2 = s.take(i + 1);
    assert(q2.last() == s[i]); // assert-line
    assert(q2.drop_last() == q1); // assert-line
    // impl-end
}
proof fn lemma_how_to_add_then_divide(x: int, y: int, d: int)
    // pre-conditions-start
    requires
        d > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        if (x % d) + (y % d) >= d {
            &&& (x + y) / d == (x / d) + (y / d) + 1
            &&& (x + y) % d == (x % d) + (y % d) - d
        } else {
            &&& (x + y) / d == (x / d) + (y / d)
            &&& (x + y) % d == (x % d) + (y % d)
        },
    // post-conditions-end
{
    // impl-start
    lemma_fundamental_div_mod(x, d);
    lemma_fundamental_div_mod(y, d);
    lemma_mul_is_distributive_add(d, x / d, y / d);
    if (x % d) + (y % d) >= d {
        lemma_mul_is_distributive_add(d, (x / d) + (y / d), 1);
        lemma_fundamental_div_mod_converse(x + y, d, (x / d) + (y / d) + 1, (x % d) + (y % d) - d);
    } else {
        lemma_fundamental_div_mod_converse(x + y, d, (x / d) + (y / d), (x % d) + (y % d));
    }
    // impl-end
}
proof fn lemma_effect_of_dividing_by_two_or_more(x: int, d: int)
    // pre-conditions-start
    requires
        d >= 2,
    // pre-conditions-end
    // post-conditions-start
    ensures
        x > 0 ==> x / d < x,
        x < 0 ==> x / d < 0,
    // post-conditions-end
{
    // impl-start
    lemma_fundamental_div_mod(x, d);
    if x > 0 {
        lemma_div_is_ordered_by_denominator(x, 2, d);
    }
    // impl-end
}
fn divide_i32_by_u32(x: i32, d: u32) -> (qr: (i32, u32))
    // pre-conditions-start
    requires
        d > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        ({
            let (q, r) = qr;
            q == x as int / d as int && r == x as int % d as int
        }),
    // post-conditions-end
{
    // impl-start
    if x >= 0 {
        return ((x as u32 / d) as i32, x as u32 % d);
    }
    let neg_x: u32;
    if x == i32::MIN {
        if d == 1 {
            return (x, 0);
        } else {
            neg_x = 0x80000000u32;
        }
    } else {
        neg_x = (-x) as u32;
    }
    assert(neg_x == -x); // assert-line
    let neg_x_div_d = neg_x / d;
    let neg_x_mod_d = neg_x % d;
    // assert-start
    assert(neg_x == d * neg_x_div_d + neg_x_mod_d) by {
        lemma_fundamental_div_mod(neg_x as int, d as int);
    }
    // assert-end
    // assert-start
    assert(neg_x_div_d <= i32::MAX) by {
        if x == i32::MIN {
            lemma_mul_inequality(2, d as int, neg_x_div_d as int);
        }
    }
    // assert-end
    if neg_x_mod_d == 0 {
        // assert-start
        proof {
            lemma_mul_unary_negation(d as int, neg_x_div_d as int);
            assert(x == d * -neg_x_div_d); // assert-line
            lemma_fundamental_div_mod_converse(x as int, d as int, -(neg_x_div_d as int), 0int);
        }
        // assert-end
        (-(neg_x_div_d as i32), 0u32)
    } else {
        // assert-start
        proof {
            lemma_mul_unary_negation(d as int, (neg_x_div_d + 1) as int);
            lemma_mul_is_distributive_add(d as int, neg_x_div_d as int, 1);
            assert(x == d as int * (-neg_x_div_d - 1) + (d - neg_x_mod_d) as int); // assert-line
            lemma_fundamental_div_mod_converse(
                x as int,
                d as int,
                -(neg_x_div_d as int) - 1,
                (d - neg_x_mod_d) as int,
            );
        }
        // assert-end
        (-(neg_x_div_d as i32) - 1, d - neg_x_mod_d)
    }
    // impl-end
}
fn divide_i32_by_usize(x: i32, d: usize) -> (qr: (i32, usize))
    // pre-conditions-start
    requires
        d > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        ({
            let (q, r) = qr;
            q == x as int / d as int && r == x as int % d as int
        }),
    // post-conditions-end
{
    // impl-start
    if d <= u32::MAX as usize {
        let (q, r) = divide_i32_by_u32(x, d as u32);
        (q, r as usize)
    } else if x >= 0 {
        // assert-start
        assert(0 == x as int / d as int && x == x as int % d as int) by {
            lemma_fundamental_div_mod_converse(x as int, d as int, 0, x as int);
        }
        // assert-end
        (0, x as usize)
    } else {
        // assert-start
        assert(-1 == x as int / d as int && d + x == x as int % d as int) by {
            lemma_fundamental_div_mod_converse(x as int, d as int, -1, d + x);
        }
        // assert-end
        let neg_x: usize = if x == i32::MIN {
            0x80000000usize
        } else {
            (-x) as usize
        };
        (-1, d - neg_x)
    }
    // impl-end
}
fn compute_mean_of_i32s(numbers: &[i32]) -> (result: i32)
    // pre-conditions-start
    requires
        numbers.len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        result == mean(numbers@.map(|_index, n: i32| n as int)),
    // post-conditions-end
{
    // impl-start
    let ghost nums = numbers@.map(|_index, n: i32| n as int);
    let mut quotient: i32 = 0;
    let mut remainder: usize = 0;
    let numbers_len: usize = numbers.len();
    for i in 0..numbers_len
        // invariants-start
        invariant
            quotient == sum(nums.take(i as int)) / numbers_len as int,
            remainder == sum(nums.take(i as int)) % numbers_len as int,
            numbers_len == numbers.len(),
            nums == numbers@.map(|_index, n: i32| n as int),
        // invariants-end
    {
        let n = numbers[i];
        // assert-start
        proof {
            lemma_how_to_update_running_sum(nums, i as int);
            lemma_sum_ratio_bound(
                nums.take(i + 1),
                numbers_len as int,
                i32::MIN as int,
                i32::MAX as int,
            );
            lemma_how_to_add_then_divide(sum(nums.take(i as int)), n as int, numbers_len as int);
        }
        // assert-end

        let (q, r) = divide_i32_by_usize(n, numbers_len);

        if r >= numbers_len - remainder {
            // assert-start
            assert(q < i32::MAX) by {
                lemma_effect_of_dividing_by_two_or_more(n as int, numbers_len as int);
            }
            // assert-end
            remainder -= (numbers_len - r);
            quotient += (q + 1);
        } else {
            remainder += r;
            quotient += q;
        }
    }
    assert(nums == nums.take(nums.len() as int)); // assert-line
    quotient
    // impl-end
}
fn compute_absolute_difference(x: i32, y: i32) -> (z: u32)
    // post-conditions-start
    ensures
        z == abs(x - y),
    // post-conditions-end
{
    // impl-start
    if x >= y {
        if y >= 0 || x < 0 {
            (x - y) as u32
        } else {
            let neg_y: u32 = if y == i32::MIN {
                0x80000000u32
            } else {
                (-y) as u32
            };
            x as u32 + neg_y
        }
    } else {
        if x >= 0 || y < 0 {
            (y - x) as u32
        } else {
            let neg_x: u32 = if x == i32::MIN {
                0x80000000u32
            } else {
                (-x) as u32
            };
            y as u32 + neg_x
        }
    }
    // impl-end
}
pub fn mean_absolute_deviation(numbers: &[i32]) -> (result: u32)
    // pre-conditions-start
    requires
        numbers.len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        result == spec_mean_absolute_deviation(numbers@.map(|_index, n: i32| n as int)),
    // post-conditions-end
{
    // impl-start
    let numbers_mean: i32 = compute_mean_of_i32s(numbers);
    let ghost deviations = numbers@.map(|_index, n: i32| n as int).map(
        |_index, n: int| abs(n - numbers_mean),
    );
    let mut quotient: u32 = 0;
    let mut remainder: usize = 0;
    let numbers_len: usize = numbers.len();
    for i in 0..numbers_len
        // invariants-start
        invariant
            quotient == sum(deviations.take(i as int)) / numbers_len as int,
            remainder == sum(deviations.take(i as int)) % numbers_len as int,
            numbers_len == numbers.len(),
            numbers_mean == mean(numbers@.map(|_index, n: i32| n as int)),
            deviations == numbers@.map(|_index, n: i32| n as int).map(
                |_index, n: int| abs(n - numbers_mean),
            ),
        // invariants-end
    {
        let n: u32 = compute_absolute_difference(numbers[i], numbers_mean);
        // assert-start
        proof {
            lemma_how_to_update_running_sum(deviations, i as int);
            lemma_sum_ratio_bound(
                deviations.take(i + 1),
                numbers_len as int,
                u32::MIN as int,
                u32::MAX as int,
            );
            lemma_how_to_add_then_divide(
                sum(deviations.take(i as int)),
                n as int,
                numbers_len as int,
            );
        }
        // assert-end

        let q: u32 = (n as usize / numbers_len) as u32;
        let r: usize = n as usize % numbers_len;

        if r >= numbers_len - remainder {
            // assert-start
            assert(q < u32::MAX) by {
                lemma_effect_of_dividing_by_two_or_more(n as int, numbers_len as int);
            }
            // assert-end
            remainder -= (numbers_len - r);
            quotient += (q + 1);
        } else {
            remainder += r;
            quotient += q;
        }
    }
    assert(deviations == deviations.take(deviations.len() as int)); // assert-line
    quotient
    // impl-end
}

}
fn main() {}
