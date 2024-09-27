method parse_paren_group(s : string) returns (max_depth : int)
    requires forall i :: i >= 0 && i < |s| ==> s[i] == '(' || s[i] == ')'
    ensures max_depth >= 0
{
    var depth: int := 0;
    max_depth := 0;
    var i: int := 0;
    while (i < |s|) 
    {
        var c: char := s[i];
        if (c == '(') {
            depth := depth + 1;
            if (depth > max_depth) {
                max_depth := depth;
            }
        } 
        else {
            depth := depth - 1;
        }
        i := i + 1;
    }
}

method split(s : string) returns (res : seq<string>) 
    requires forall i :: i >= 0 && i < |s| ==> s[i] == '(' || s[i] == ')' || s[i] == ' '
    ensures forall s1 :: s1 in res ==> (forall i :: i >= 0 && i < |s1| ==> s1[i] == '(' || s1[i] == ')') && |s1| > 0
{
    res := [];
    var current_string : string := "";
    var i : int := 0;
    while (i < |s|) 
        invariant i >= 0 && i <= |s|
        invariant forall j :: j >= 0 && j < |current_string| ==> current_string[j] == '(' || current_string[j] == ')'
        invariant forall s1 :: s1 in res ==> (forall j :: j >= 0 && j < |s1| ==> s1[j] == '(' || s1[j] == ')') && |s1| > 0
    {
        if (s[i] == ' ') 
        {
            if (current_string != "") {
                res := res + [current_string];
                current_string := "";
            }
        } 
        else 
        {
            current_string := current_string + [s[i]];
        }
        i := i + 1;
    }
    if (current_string != "") {
        res := res + [current_string];
        current_string := "";
    }
}

method parse_nested_parens(paren_string: string) returns (res : seq<int>)
    requires forall i :: i >= 0 && i < |paren_string| ==> paren_string[i] == '(' || paren_string[i] == ')' || paren_string[i] == ' '
    ensures forall x :: x in res ==> x >= 0
{
    var strings : seq<string> := split(paren_string);
    var i : int := 0;
    res := [];
    while (i < |strings|) 
        invariant forall x :: x in res ==> x >= 0
    {
        var cur : int := parse_paren_group(strings[i]);
        res := res + [cur];
        i := i + 1;
    }
}
    
 