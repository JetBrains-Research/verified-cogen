method xor(a : char, b : char) returns (result : char)
    ensures result == (if a == b then '0' else '1')
{
    if (a == b) {
        result := '0';
    } else {
        result := '1';
    }
}

method string_xor(a: string, b: string) returns (result: string)
    requires |a| == |b| 
    requires forall i :: 0 <= i < |a| ==> (a[i] == '0' || a[i] == '1')  
    requires forall i :: 0 <= i < |b| ==> (b[i] == '0' || b[i] == '1')  
    ensures |result| == |a|
    ensures forall i :: 0 <= i < |result| ==> (result[i] == '0' || result[i] == '1') 
    ensures forall i :: 0 <= i < |result| ==> result[i] == (if a[i] == b[i] then '0' else '1')
{
    result := "";
    var i : int := 0;
    while (i < |a|) 
        invariant i >= 0 && i <= |a|
        invariant |result| == i
        invariant forall j :: 0 <= j < i ==> result[j] == (if a[j] == b[j] then '0' else '1')
    {
        var bitResult := if a[i] == b[i] then '0' else '1';
        result := result + [bitResult];
        i := i + 1;
    }
}