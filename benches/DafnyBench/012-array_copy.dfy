method iter_copy<T(0)>(s: array<T>) returns (t: array<T>)
  // pre-conditions-start
  // pre-conditions-end
  // post-conditions-start
  ensures s.Length==t.Length
  ensures forall i::0<=i<s.Length ==> s[i]==t[i]
  // post-conditions-end
{
  // impl-start
  t := new T[s.Length];
  var i:= 0;
  while (i < s.Length)
    // invariants-start
    invariant 0 <= i <= s.Length
    invariant forall x :: 0 <= x < i ==> s[x] == t[x]
    // invariants-end
  {
    t[i] := s[i];
    i:=i+1;
  }
  // impl-end
}
