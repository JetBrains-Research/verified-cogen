method allDigits(s: string) returns (result: bool)
  // post-conditions-start
  ensures  result <==> (forall i :: 0 <= i < |s| ==> s[i] in "0123456789")
  // post-conditions-end
{
  // impl-start
  result:=true;
  for i := 0 to |s|
    // invariants-start
    invariant result <==> (forall ii :: 0 <= ii < i ==> s[ii] in "0123456789")
    // invariants-end
  {
    if ! (s[i] in "0123456789"){
      return false;
    }
  }
  // impl-end
}
