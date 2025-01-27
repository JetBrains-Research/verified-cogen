use vstd::prelude::*;

verus! {
spec fn sorted_between(a: Seq<u32>, from: int, to: int) -> (result:bool) {
    forall |i: int, j:int|  from <= i < j < to ==> a[i] <= a[j]
}
// pure-end

spec fn is_reorder_of<T>(r: Seq<int>, p: Seq<T>, s: Seq<T>) -> (result:bool) {
    &&& r.len() == s.len()
    &&& forall|i: int| 0 <= i < r.len() ==> 0 <= #[trigger] r[i] < r.len()
    &&& forall|i: int, j: int| 0 <= i < j < r.len() ==> r[i] != r[j]
    &&& p =~= r.map_values(|i: int| s[i])
}
// pure-end

fn test1(nums: &mut Vec<u32>)
    // post-conditions-start
    ensures
        sorted_between(nums@, 0, nums@.len() as int),
        exists|r: Seq<int>| is_reorder_of(r, nums@, old(nums)@),
    // post-conditions-end
{
    // impl-start
    // assert-start
    proof {
        let r = Seq::new(nums@.len(), |i: int| i);
        assert(is_reorder_of(r, nums@, nums@));
    }
    // assert-end
    let n = nums.len();
    if n == 0 {
        return;
    }
    for i in 1..n
        // invariants-start
        invariant
            n == nums.len(),
            sorted_between(nums@, 0, i as int),
            exists|r: Seq<int>| is_reorder_of(r, nums@, old(nums)@),
        // invariants-end
    {
        let mut j = i;
        while j != 0
            // invariants-start
            invariant
                0 <= j <= i < n == nums.len(),
                forall|x: int, y: int| 0 <= x <= y <= i ==> x != j && y != j ==> nums[x] <= nums[y],
                sorted_between(nums@, j as int, i + 1),
                exists|r: Seq<int>| is_reorder_of(r, nums@, old(nums)@),
            // invariants-end
        {
            if nums[j - 1] > nums[j] {
                // assert-start
                proof {
                    let r1 = choose|r: Seq<int>| is_reorder_of(r, nums@, old(nums)@);
                    let r2 = r1.update(j-1, r1[j as int]).update(j as int, r1[j-1]);
                    assert(is_reorder_of(r2, nums@.update(j-1, nums@[j as int]).update(j as int, nums@[j-1]), old(nums)@));
                }
                // assert-end
                let temp = nums[j - 1];
                nums.set(j - 1, nums[j]);
                nums.set(j, temp);
            }
            j -= 1;
        }
    }
    // impl-end
}
}


fn main() {}