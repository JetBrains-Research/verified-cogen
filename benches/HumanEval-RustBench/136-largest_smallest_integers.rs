use vstd::prelude::*;

verus! {

fn largest_smallest_integers(arr: &Vec<i32>) -> (res: (Option<i32>, Option<i32>))
    ensures
        ({
            let a = res.0;
            let b = res.1;
            &&& a.is_none() ==> forall|i: int| 0 <= i < arr@.len() ==> arr@[i] >= 0
            &&& a.is_some() ==> arr@.contains(a.unwrap()) && a.unwrap() < 0
            &&& a.is_some() ==> forall|i: int|
                0 <= i < arr@.len() && arr@[i] < 0 ==> arr@[i] <= a.unwrap()
            &&& b.is_none() ==> forall|i: int| 0 <= i < arr@.len() ==> arr@[i] <= 0
            &&& b.is_some() ==> arr@.contains(b.unwrap()) && b.unwrap() > 0
            &&& b.is_some() ==> forall|i: int|
                0 <= i < arr@.len() && arr@[i] > 0 ==> arr@[i] >= b.unwrap()
        }),
{
    let mut i: usize = 0;
    let mut a = None;
    let mut b = None;

    while i < arr.len()
        invariant
            0 <= i <= arr@.len(),
            a.is_none() ==> forall|j: int| 0 <= j < i ==> arr@[j] >= 0,
            a.is_some() ==> arr@.contains(a.unwrap()) && a.unwrap() < 0,
            a.is_some() ==> forall|j: int| 0 <= j < i && arr@[j] < 0 ==> arr@[j] <= a.unwrap(),
            b.is_none() ==> forall|j: int| 0 <= j < i ==> arr@[j] <= 0,
            b.is_some() ==> arr@.contains(b.unwrap()) && b.unwrap() > 0,
            b.is_some() ==> forall|j: int| 0 <= j < i && arr@[j] > 0 ==> arr@[j] >= b.unwrap(),
    {
        if arr[i] < 0 && (a.is_none() || arr[i] >= a.unwrap()) {
            a = Some(arr[i]);
        }
        if arr[i] > 0 && (b.is_none() || arr[i] <= b.unwrap()) {
            b = Some(arr[i]);
        }
        i = i + 1;
    }
    (a, b)
}

} 
fn main() {}
