method Sum(N:int) returns (s:int)
  // pre-conditions-start
  requires N >= 0
  // pre-conditions-end
  // post-conditions-start
  ensures s == N * (N + 1) / 2
  // post-conditions-end
{
  // impl-start
  var n := 0;
  s := 0;
  while n != N
    // invariants-start
    invariant 0 <= n <= N
    invariant s == n * (n + 1) / 2
    // invariants-end
  {
    n := n + 1;
    s := s + n;
  }
  // impl-end
}
