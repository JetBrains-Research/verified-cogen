
method checkSubstring(s: string, sub: string) returns (result: bool)
{
    result := false;
    if (|sub| == 0) 
    {
        result := true;
    }
    else if (|s| >= |sub|) 
    {
        var i: int := 0;
        while (i <= |s| - |sub|)
        {
            if (s[i..i + |sub|] == sub) 
            {
                result := true;
            }
            i := i + 1;
        }
    }
}

method filter_by_substring(strings: seq<string>, substring: string) returns (res : seq<string>)
    ensures |res| <= |strings|
    ensures (forall s :: s in res ==> s in strings)
{
    res := [];
    var i : int := 0;
    while (i < |strings|) 
        invariant 0 <= i && i <= |strings|
        invariant |res| <= i
        invariant (forall s :: s in res ==> s in strings)
    {
        var check : bool := checkSubstring(strings[i], substring);
        if (check) 
        {
            res := res + [strings[i]];
        }
        i := i + 1;
    }
}

