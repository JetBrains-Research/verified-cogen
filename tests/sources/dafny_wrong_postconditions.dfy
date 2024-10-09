function ParenthesesDepth(s: string, i: int, j: int): int
  decreases j - i
  requires 0 <= i <= j <= |s|
{
  if i == j then
    0
  else if s[i] == '(' then
    ParenthesesDepth(s, i+1, j) + 1
  else if s[i] == ')' then
    ParenthesesDepth(s, i+1, j) - 1
  else
    ParenthesesDepth(s, i+1, j)
}

predicate InnerDepthsPositive(s: string)
{
  forall i :: 0 < i < |s| ==> ParenthesesDepth(s, 0, i) > 0
}

predicate InnerDepthsNonnegative(s: string)
{
  forall i :: 0 < i < |s| ==> ParenthesesDepth(s, 0, i) >= 0
}

lemma ParenthesesDepthSum(s: string, i: int, j: int, k: int)
  decreases j - i
  requires 0 <= i <= j <= k <= |s|
  ensures ParenthesesDepth(s, i, k) == ParenthesesDepth(s, i, j) + ParenthesesDepth(s, j, k)
{
  if i != j {
    ParenthesesDepthSum(s, i+1, j, k);
  }
}

lemma ParenthesesSuffixEq(s: string, i: int, j: int)
  decreases j -i
  requires 0 <= i <= j <= |s|
  ensures ParenthesesDepth(s, i, j) == ParenthesesDepth(s[..j], i, j)
{
  if i != j {
    ParenthesesSuffixEq(s, i+1, j);
  }
}

lemma ParenthesesPrefixEq(s: string, i: int, j: int)
  decreases j -i
  requires 0 <= i <= j <= |s|
  ensures ParenthesesDepth(s, i, j) == ParenthesesDepth(s[i..], 0, j-i)
{ }

lemma ParenthesesSubstring(s: string, i: int, j: int)
  decreases j - i
  requires 0 <= i <= j <= |s|
  ensures ParenthesesDepth(s, i, j) == ParenthesesDepth(s[i..j], 0, j-i)
{
  assert ParenthesesDepth(s, i, j) == ParenthesesDepth(s[..j], i, j)
  by { ParenthesesSuffixEq(s, i, j); }
  assert ParenthesesDepth(s[..j], i, j) == ParenthesesDepth(s[i..j], 0, j-i)
  by { ParenthesesPrefixEq(s[..j], i, j); }
}

lemma ParenthesesCommonSegment(s: string, t: string, i: int, j: int)
  requires 0 <= i <= j <= |s|
  requires 0 <= i <= j <= |t|
  requires s[i..j] == t[i..j]
  ensures ParenthesesDepth(s, i, j) == ParenthesesDepth(t, i, j)
{
  ParenthesesSubstring(s, i, j);
  ParenthesesSubstring(t, i, j);
}

lemma ParenthesesDepthAppend(s: string, c: char)
  ensures ParenthesesDepth(s + [c], 0, |s|+1) == ParenthesesDepth(s, 0, |s|) + ParenthesesDepth([c], 0, 1)
{
  ParenthesesSubstring(s + [c], 0, |s|);
  ParenthesesSubstring(s + [c], |s|, |s| + 1);
  ParenthesesDepthSum(s + [c], 0, |s|, |s| + 1);
}

lemma InnerDepthsPositiveAppendDecompose(s: string, c: char)
  requires InnerDepthsPositive(s)
  requires ParenthesesDepth(s, 0, |s|) > 0
  ensures InnerDepthsPositive(s + [c])
{
  forall i: int | 0 < i < |s| + 1
    ensures ParenthesesDepth(s + [c], 0, i) > 0
  {
    if (i <= |s|) {
      ParenthesesCommonSegment(s, s + [c], 0, i);
    }
  }
}

method separate_paren_groups(paren_string: string) returns (res : seq<string>)
  // pre-conditions-start
  requires ParenthesesDepth(paren_string, 0, |paren_string|) == 0
  requires InnerDepthsNonnegative(paren_string)
  // pre-conditions-end
{
  // impl-start
  res := [];
  var current_string: string := "";
  var current_depth: int := 0;

  var i: int := 0;

  while (i < |paren_string|)
    // invariants-start
    invariant 0 <= i <= |paren_string|
    invariant forall k :: 0 <= k < |res| ==> ParenthesesDepth(res[k], 0, |res[k]|) == 0
    invariant forall k :: 0 <= k < |res| ==> InnerDepthsPositive(res[k])
    invariant ParenthesesDepth(paren_string, 0, |paren_string|) == 0
    invariant InnerDepthsNonnegative(paren_string)
    invariant ParenthesesDepth(paren_string, i, |paren_string|) + current_depth == 0
    invariant ParenthesesDepth(paren_string, 0, i) == current_depth
    invariant ParenthesesDepth(current_string, 0, |current_string|) == current_depth
    invariant InnerDepthsPositive(current_string)
    invariant current_string == "" || current_depth > 0
    invariant current_depth >= 0
    // invariants-end
  {
    var c: char := paren_string[i];

    // lemma-use-start
    ParenthesesDepthAppend(current_string, c);
    ParenthesesDepthSum(paren_string, 0, i, i+1);
    if (current_string != "") {
      InnerDepthsPositiveAppendDecompose(current_string, c);
    }
    // lemma-use-end

    if (c == '(')
    {
      current_depth := current_depth + 1;
      current_string := current_string + [c];
    }
    else if (c == ')')
    {
      current_depth := current_depth - 1;
      current_string := current_string + [c];

      if (current_depth == 0)
      {
        res := res + [current_string];
        current_string := "";
      }
    }
    i := i + 1;
  }
  // impl-end
}

// ==== verifiers ====
method separate_paren_groups_valid(paren_string: string) returns (res : seq<string>)
  // pre-conditions-start
  requires ParenthesesDepth(paren_string, 0, |paren_string|) == 0
  requires InnerDepthsNonnegative(paren_string)
  // pre-conditions-end
  // post-conditions-start
  ensures forall k :: 0 <= k < |res| ==> ParenthesesDepth(res[k], 0, |res[k]|) == 0
  ensures forall k :: 0 <= k < |res| ==> InnerDepthsPositive(res[k])
  // post-conditions-end
{ var ret0 := separate_paren_groups(paren_string); return ret0; }
