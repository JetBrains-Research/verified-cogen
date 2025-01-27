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
        let ghost mut r = Seq::new(nums@.len(), |i: int| i);
        // assert-start
        assert(is_reorder_of(r, nums@, nums@));
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
                is_reorder_of(r, nums@, old(nums)@),
            // invariants-end
        {
            let mut j = i;
            while j != 0
                // invariants-start
                invariant
                    0 <= j <= i < n == nums.len(),
                    forall|x: int, y: int| 0 <= x <= y <= i ==> x != j && y != j ==> nums[x] <= nums[y],
                    sorted_between(nums@, j as int, i + 1),
                    is_reorder_of(r, nums@, old(nums)@),
                // invariants-end
            {
                if nums[j - 1] > nums[j] {
                    let temp = nums[j - 1];
                    nums.set(j - 1, nums[j]);
                    nums.set(j, temp);
                    // assert-start
                    proof {
                        r = r.update(j - 1, r[j as int]).update(j as int, r[j - 1]);
                    }
                    // assert-end
                }
                j -= 1;
            }
        }
        // impl-end
    }
}

fn main() {}