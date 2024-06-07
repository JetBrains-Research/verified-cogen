datatype Option<T> = None | Some(T)

function getVal(mx : Option<string>) : string
    requires mx != None
{
    match mx {
        case Some(n) => n
    }
}

method longest(strings: seq<string>) returns (result : Option<string>)
  ensures result == None <==> |strings| == 0 
  ensures result != None ==> (forall s :: s in strings ==> |getVal(result)| >= |s|)
  ensures result != None ==> (exists s :: s in strings && |s| == |getVal(result)|) 
  ensures result != None ==> (exists i :: 0 <= i < |strings| && strings[i] == getVal(result) && forall j :: 0 <= j < i ==> |strings[j]| < |getVal(result)|) 
{
    result := None;
    if (|strings| != 0)
    {
        var i : int := 0;
        var mx : int := -1;
        while (i < |strings|) 
            invariant i >= 0 && i <= |strings|
            invariant (mx == -1) == (result == None)
            invariant i == 0 ==> mx == -1
            invariant i > 0 ==> (forall s :: s in strings[0..i] ==> mx >= |s|)
            invariant i > 0 ==> (exists s :: s in strings && mx == |s|)
            invariant i > 0 ==> mx == |getVal(result)|
            invariant result != None ==> (exists i :: 0 <= i < |strings| && strings[i] == getVal(result) && forall j :: 0 <= j < i ==> |strings[j]| < |getVal(result)|) 
        {
            if (|strings[i]| > mx) {
                mx := |strings[i]|;
                result := Some(strings[i]);
            }
            i := i + 1;
        }
    }
}

