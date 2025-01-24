method BinarySearch(a: array<int>, key: int) returns (n: int)
  // pre-conditions-start
  requires forall i,j :: 0<=i<j<a.Length ==> a[i]<=a[j]
  // pre-conditions-end
  // post-conditions-start
  ensures 0<= n <=a.Length
  ensures forall i :: 0<= i < n ==> a[i] < key
  ensures n == a.Length ==> forall i :: 0 <= i < a.Length ==> a[i] < key
  ensures forall i :: n<= i < a.Length ==> a[i]>=key
  // post-conditions-end
{
  // impl-start
  var lo, hi := 0, a.Length;
  while lo<hi
    // invariants-start
    invariant 0<= lo <= hi <= a.Length
    invariant forall i :: 0<=i<lo ==> a[i] < key
    invariant forall i :: hi<=i<a.Length ==> a[i] >= key
    // invariants-end
  {
    var mid := (lo + hi) / 2;
    if a[mid] < key {
      lo := mid + 1;
    } else {
      hi := mid;
    }
  }
  n:=lo;
  // impl-end
}
