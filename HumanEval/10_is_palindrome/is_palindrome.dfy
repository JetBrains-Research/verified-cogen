method is_palindrome(s: string) returns (result: bool)
    requires |s| > 0
    ensures result == (forall k :: 0 <= k < |s| ==> s[k] == s[|s| - 1 - k])
{
    result := true;
    var i := 0;
    var j := |s| - 1;
    while (i < j)
        invariant 0 <= i < |s|
        invariant 0 <= j < |s|
        invariant j == |s| - i - 1
        invariant forall k :: 0 <= k < i ==> s[k] == s[|s| - 1 - k]
    {
        if (s[i] != s[j]) {
            result := false;
            break;
        }
        i := i + 1;
        j := j - 1;
    }
}

function is_palindrome_fun(s : string) : bool {
    forall k :: 0 <= k < |s| ==> s[k] == s[|s| - 1 - k]   
}

function starts_with(result : string, s : string) : bool {
    |result| >= |s| && forall k :: 0 <= k < |s| ==> result[k] == s[k]   
}

method make_palindrome(s: string) returns (result: string)
    ensures |result| <= 2 * |s|  
    ensures is_palindrome_fun(result)
    ensures starts_with(result, s)
{
    if (|s| == 0) {
        return "";
    }

    var beginning_of_suffix := 0;
    var longest_palindrome := "";
    var flag := is_palindrome(s[beginning_of_suffix..]);

    
    while (!flag)
        invariant (beginning_of_suffix >= 0 && beginning_of_suffix + 1 < |s|) || (flag && (beginning_of_suffix >= 0 && beginning_of_suffix < |s|))
        decreases |s| - beginning_of_suffix
        invariant flag ==> is_palindrome_fun(s[beginning_of_suffix..])
    {
        beginning_of_suffix := beginning_of_suffix + 1;
        flag := is_palindrome(s[beginning_of_suffix..]);
    }

    var prefix_to_reverse := s[..beginning_of_suffix];
    var reversed := reverse(prefix_to_reverse);
    result := s + reversed;
}

method reverse(str: string) returns (rev: string)
    ensures |rev| == |str|
    ensures forall k :: 0 <= k < |str| ==> rev[k] == str[|str| - 1 - k]
{
    rev := "";
    var i := 0;
    while (i < |str|) 
        invariant i >= 0 && i <= |str|
        invariant |rev| == i
        invariant forall k :: 0 <= k < i ==> rev[k] == str[|str| - 1 - k]
    {
        rev := rev + [str[|str| - i - 1]];
        i := i + 1;
    }
}