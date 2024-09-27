datatype Option<T> = None | Some(T)


function getVal(mx : Option<int>) : int 
    requires exists i : int :: mx == Some(i)
{
    match mx {
        case Some(n) => n
    }
}

method rolling_max(numbers: seq<int>) returns (result : seq<int>)
    ensures |numbers| == |result|
    ensures forall i : int :: i >= 0 && i < |numbers| ==> numbers[i] <= result[i]
    ensures forall i : int :: i >= 0 && i + 1 < |numbers| ==> result[i] <= result[i + 1]
{
    var running_max: Option<int> := None;
    result := [];

    var i : int := 0;
    while (i < |numbers|) 
        invariant i >= 0 && i <= |numbers|
        invariant |result| == i
        invariant forall i1 : int :: i1 >= 0 && i1 < i ==> numbers[i1] <= result[i1]
        invariant old(running_max) == None || (exists i : int :: old(running_max) == Some(i) && getVal(old(running_max)) <= getVal(running_max))
        invariant |result| > 0 ==> exists i : int :: running_max == Some(i)
        invariant |result| > 0 ==> result[|result| - 1] == getVal(running_max)
        invariant forall i1 : int :: i1 >= 0 && i1 + 1 < i ==> result[i1] <= result[i1 + 1]
    {
        var n : int := numbers[i];
        match running_max {
            case None => running_max := Some(n);
            case Some(n1) => 
            {
                if (n1 < n) {
                    running_max := Some(n);
                }
            }
        }
        match running_max {
            case Some(n1) => result := result + [n1];
        }
        i := i + 1;
    }
}