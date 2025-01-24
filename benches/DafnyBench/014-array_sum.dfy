method arraySum(a: array<int>, b: array<int>) returns (c: array<int> )
  // pre-conditions-start
  requires a.Length==b.Length
  // pre-conditions-end
  // post-conditions-start
  ensures c.Length==a.Length
  ensures forall i:: 0 <= i< a.Length==> a[i] + b[i]==c[i]
  // post-conditions-end
{
  // impl-start
  c:= new int[a.Length];
  var i:=0;
  while i<a.Length
    // invariants-start
    invariant 0<=i<=a.Length
    invariant forall j:: 0 <= j< i==> a[j] + b[j]==c[j]
    // invariants-end
  {
    c[i]:=a[i]+b[i];
    i:=i+1;
  }
  // impl-end
}
