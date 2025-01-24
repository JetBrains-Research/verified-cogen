method append(a:array<int>, b:int) returns (c:array<int>)
  // pre-conditions-start
  // pre-conditions-end
  // post-conditions-start
  ensures  a[..] + [b] == c[..]
  // post-conditions-end
{
  // impl-start
  c := new int[a.Length+1];
  var i:= 0;
  while (i < a.Length)
    // invariants-start
    invariant 0 <= i <= a.Length
    invariant forall ii::0<=ii<i ==> c[ii]==a[ii]
    // invariants-end
  {
    c[i] := a[i];
    i:=i+1;
  }
  c[a.Length]:=b;
  // impl-end
}
