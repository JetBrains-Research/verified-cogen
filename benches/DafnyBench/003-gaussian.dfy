method gaussian(size: int, q: array<real>, q_hat: array<real>) returns (out: array<real>)
  // pre-conditions-start
  requires q_hat.Length == size
  requires q.Length == size
  requires size > 0
  requires arraySquaredSum(q_hat[..]) <= 1.0
  // pre-conditions-end
{
  // impl-start
  var i: int := 0;
  var alpha: real := arraySquaredSum(q_hat[..1]);
  var eta: real := 0.0;
  var eta_hat: real := 0.0;
  out := new real[size];
  while (i < size)
    // invariants-start
    invariant 0 < i <= size ==> alpha <= arraySquaredSum(q_hat[..i])
    invariant i <= size
    // invariants-end
  {
    eta := *;
    eta_hat := -q_hat[i];
    alpha := arraySquaredSum(q_hat[..i+1]);
    // assert-start
    assert (q_hat[i] + eta_hat == 0.0);
    // assert-end
    out[i] := q[i] + eta;
    i := i + 1;
  }
  // assert-start
  assert i == size;
  assert alpha <= arraySquaredSum(q_hat[..size]);
  assert q_hat[..size] == q_hat[..];
  assert alpha <= arraySquaredSum(q_hat[..]);
  assert alpha <= 1.0;
  // assert-end
  // impl-end
}

function arraySquaredSum(a: seq<real>): real
  // pre-conditions-start
  requires |a| > 0
  // pre-conditions-end
{
  if |a| == 1 then
    a[0] * a[0]
  else
    (a[0] * a[0]) + arraySquaredSum(a[1..])
}
