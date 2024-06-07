method all_prefixes(s: string) returns (prefixes: seq<string>)
    ensures |prefixes| == |s| 
    ensures forall i :: 0 <= i < |prefixes| ==> s[..i+1] == prefixes[i]
{
    prefixes := [];
    for i := 0 to |s|
        invariant |prefixes| == i
        invariant forall j :: 0 <= j < i ==> prefixes[j] == s[..j+1]
    {
        var current_prefix := s[..i+1];
        prefixes := prefixes + [current_prefix];
    }
}