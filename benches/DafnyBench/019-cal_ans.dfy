method CalDiv() returns (x:int, y:int)
  // post-conditions-start
  ensures x==191/7
  ensures y==191%7
  // post-conditions-end
{
  // impl-start
  x, y := 0, 191;
  while 7 <= y
    // invariants-start
    invariant 0 <= y && 7 * x + y == 191
    // invariants-end
  {
    x := x+1;
    y:=191-7*x;
  }
  // impl-end
}
