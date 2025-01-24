method Abs(x: int) returns (y: int)
  // post-conditions-start
  ensures x>=0 ==> x==y
  ensures x<0 ==> x+y==0
  // post-conditions-end
{
  // impl-start
  if x < 0 {
    return -x;
  } else {
    return x;
  }
  // impl-end
}
