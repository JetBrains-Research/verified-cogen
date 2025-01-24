predicate Sorted(q: seq<int>) {
  forall i,j :: 0 <= i <= j < |q| ==> q[i] <= q[j]
}

method MergeSort(a: array<int>) returns (b: array<int>)
  // pre-conditions-start
  // pre-conditions-end
  // post-conditions-start
  ensures b.Length == a.Length && Sorted(b[..]) && multiset(a[..]) == multiset(b[..])
  // post-conditions-end
  decreases a.Length
{
  // impl-start
  if (a.Length <= 1) {b := a;}
  else{
    var mid: nat := a.Length / 2;
    var a1: array<int> := new int[mid];
    var a2: array<int> := new int[a.Length - mid];
    assert a1.Length <= a2.Length;
    assert a.Length == a1.Length + a2.Length;

    var i: nat := 0;
    while (i < a1.Length )
      // invariants-start
      invariant Inv(a[..], a1[..], a2[..], i, mid)
      // invariants-end
      decreases a1.Length - i
    {
      a1[i] := a[i];
      a2[i] := a[i+mid];
      i:=i+1;
    }
    assert !(i < a1.Length);
    assert (i >= a1.Length);
    assert i == a1.Length;
    assert Inv(a[..], a1[..], a2[..], i, mid);
    assert (i <= |a1[..]|) && (i <= |a2[..]|) && (i+mid <= |a[..]|);
    assert (a1[..i] == a[..i]) && (a2[..i] == a[mid..(i+mid)]);

    if(a1.Length < a2.Length) {
      a2[i] := a[i+mid];
      assert i+1 == a2.Length;
      assert (a2[..i+1] == a[mid..(i+1+mid)]);
      assert (a1[..i] == a[..i]) && (a2[..i+1] == a[mid..(i+1+mid)]);
      assert a[..i] + a[i..i+1+mid] == a1[..i] + a2[..i+1];
      assert a[..i] + a[i..i+1+mid] == a1[..] + a2[..];
      assert a[..] == a1[..] + a2[..];
    }
    else{
      assert i == a2.Length;
      assert (a1[..i] == a[..i]) && (a2[..i] == a[mid..(i+mid)]);
      assert a[..i] + a[i..i+mid] == a1[..i] + a2[..i];
      assert a[..i] + a[i..i+mid] == a1[..] + a2[..];
      assert a[..] == a1[..] + a2[..];
    }

    assert a1.Length < a.Length;
    a1:= MergeSort(a1);
    assert a2.Length < a.Length;
    a2:= MergeSort(a2);
    b := new int [a.Length];
    Merge(b, a1, a2);
    assert multiset(b[..]) == multiset(a1[..]) + multiset(a2[..]);
    assert Sorted(b[..]);
  }
  assert b.Length == a.Length && Sorted(b[..]) && multiset(a[..]) == multiset(b[..]);
  // impl-end
}

ghost predicate Inv(a: seq<int>, a1: seq<int>, a2: seq<int>, i: nat, mid: nat){
  (i <= |a1|) && (i <= |a2|) && (i+mid <= |a|) &&
  (a1[..i] == a[..i]) && (a2[..i] == a[mid..(i+mid)])
}

method Merge(b: array<int>, c: array<int>, d: array<int>)
  // pre-conditions-start
  requires b != c && b != d && b.Length == c.Length + d.Length
  requires Sorted(c[..]) && Sorted(d[..])
  // pre-conditions-end
  // post-conditions-start
  ensures Sorted(b[..]) && multiset(b[..]) == multiset(c[..])+multiset(d[..])
  // post-conditions-end
  modifies b
{
  // impl-start
  var i: nat, j: nat := 0, 0;
  while i + j < b.Length
    // invariants-start
    invariant i <= c.Length && j <= d.Length && i + j <= b.Length
    invariant InvSubSet(b[..],c[..],d[..],i,j)
    invariant InvSorted(b[..],c[..],d[..],i,j)
    // invariants-end
    decreases c.Length-i, d.Length-j
  {
    i,j := MergeLoop (b,c,d,i,j);
    assert InvSubSet(b[..],c[..],d[..],i,j);
    assert InvSorted(b[..],c[..],d[..],i,j);
  }
  assert InvSubSet(b[..],c[..],d[..],i,j);
  LemmaMultysetsEquals(b[..],c[..],d[..],i,j);
  assert multiset(b[..]) == multiset(c[..])+multiset(d[..]);
  // impl-end
}

method {:verify true} MergeLoop(b: array<int>, c: array<int>, d: array<int>,i0: nat , j0: nat)  returns (i: nat, j: nat)
  requires b != c && b != d && b.Length == c.Length + d.Length
  requires Sorted(c[..]) && Sorted(d[..])
  requires i0 <= c.Length && j0 <= d.Length && i0 + j0 <= b.Length
  requires InvSubSet(b[..],c[..],d[..],i0,j0)
  requires InvSorted(b[..],c[..],d[..],i0,j0)
  requires i0 + j0 < b.Length

  modifies b

  ensures i <= c.Length && j <= d.Length && i + j <= b.Length
  ensures InvSubSet(b[..],c[..],d[..],i,j)
  ensures InvSorted(b[..],c[..],d[..],i,j)
  ensures 0 <= c.Length - i < c.Length - i0 || (c.Length - i == c.Length - i0 && 0 <= d.Length - j < d.Length - j0)
{

  i,j := i0,j0;

  if(i == c.Length || (j< d.Length && d[j] < c[i])){

    assert InvSorted(b[..][i+j:=d[j]],c[..],d[..],i,j+1);
    b[i+j] := d[j];
    lemmaInvSubsetTakeValueFromD(b[..],c[..],d[..],i,j);

    assert InvSubSet(b[..],c[..],d[..],i,j+1);
    assert InvSorted(b[..],c[..],d[..],i,j+1);
    j := j + 1;
  }
  else{
    assert j == d.Length || (i < c.Length && c[i] <= d[j]);

    assert InvSorted(b[..][i+j:=c[i]],c[..],d[..],i+1,j);

    b[i+j] := c[i];

    lemmaInvSubsetTakeValueFromC(b[..],c[..],d[..],i,j);
    assert InvSubSet(b[..],c[..],d[..],i+1,j);
    assert InvSorted(b[..],c[..],d[..],i+1,j);
    i := i + 1;
  }
}

ghost predicate InvSorted(b: seq<int>, c: seq<int>, d: seq<int>, i: nat, j: nat){
  i <= |c| && j <= |d| && i + j <= |b| &&
  ((i+j > 0 && i < |c|) ==> (b[j + i - 1] <= c[i])) &&
  ((i+j > 0 && j < |d|) ==> (b[j + i - 1] <= d[j])) &&
  Sorted(b[..i+j])
}

ghost predicate InvSubSet(b: seq<int>, c: seq<int>, d: seq<int>, i: nat, j: nat){
  i <= |c| && j <= |d| && i + j <= |b| &&
  multiset(b[..i+j]) == multiset(c[..i]) + multiset(d[..j])
}
lemma LemmaMultysetsEquals (b: seq<int>, c: seq<int>, d: seq<int>, i: nat, j: nat)
  requires i == |c|
  requires j == |d|
  requires i + j == |b|
  requires multiset(b[..i+j]) == multiset(c[..i]) + multiset(d[..j])
  ensures multiset(b[..]) == multiset(c[..])+multiset(d[..]);
{
  assert b[..] == b[..i+j];
  assert c[..] == c[..i];
  assert d[..] == d[..j];
}

lemma lemmaInvSubsetTakeValueFromC (b: seq<int>, c: seq<int>, d: seq<int>, i: nat, j: nat)
  requires i < |c|;
  requires j <= |d|;
  requires i + j < |b|;
  requires |c| + |d| == |b|;
  requires multiset(b[..i+j]) == multiset(c[..i]) + multiset(d[..j])
  requires b[i+j] == c[i]
  ensures multiset(b[..i+j+1]) == multiset(c[..i+1])+multiset(d[..j])
{
  assert c[..i]+[c[i]] == c[..i+1];
  assert b[..i+j+1] == b[..i+j] + [b[i+j]];
  assert multiset(b[..i+j+1]) == multiset(c[..i+1])+multiset(d[..j]);
}


lemma{:verify true} lemmaInvSubsetTakeValueFromD (b: seq<int>, c: seq<int>, d: seq<int>, i: nat, j: nat)
  requires i <= |c|;
  requires j < |d|;
  requires i + j < |b|;
  requires |c| + |d| == |b|;
  requires multiset(b[..i+j]) == multiset(c[..i]) + multiset(d[..j])
  requires b[i+j] == d[j]
  ensures multiset(b[..i+j+1]) == multiset(c[..i])+multiset(d[..j+1])
{
  assert d[..j]+[d[j]] == d[..j+1];
  assert b[..i+j+1] == b[..i+j] + [b[i+j]];
  assert multiset(b[..i+j+1]) == multiset(c[..i])+multiset(d[..j+1]);
}





method Main() {
  var a := new int[3] [4, 8, 6];
  var q0 := a[..];
  assert q0 == [4,8,6];
  a := MergeSort(a);
  assert a.Length == |q0| && multiset(a[..]) == multiset(q0);
  print "\nThe sorted version of ", q0, " is ", a[..];
  assert Sorted(a[..]);
  assert a[..] == [4, 6, 8];

  a := new int[5] [3, 8, 5, -1, 10];
  q0 := a[..];
  assert q0 == [3, 8, 5, -1, 10];
  a := MergeSort(a);
  assert a.Length == |q0| && multiset(a[..]) == multiset(q0);
  print "\nThe sorted version of ", q0, " is ", a[..];
  assert Sorted(a[..]);
}
