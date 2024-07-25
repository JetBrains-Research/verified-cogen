method abs(val : int) returns (res : int)
    ensures val < 0 ==> res == -val
    ensures val >= 0 ==> res == val
{
    if (val < 0) {
        res := -val;
    } else {
        res := val;
    }
}

function abs1(x : int, threshold : int): bool 
{
    x >= threshold || x <= -threshold
}

method has_close_elements(numbers: seq<int>, threshold: int) returns (flag : bool)
    requires threshold > 0
    ensures flag == (exists i: int, j: int :: i >= 0 && j >= 0 && i < |numbers| && j < |numbers| && i != j && !abs1(numbers[i] - numbers[j], threshold))
{
    flag := false;
    var i: int := 0;
    while (i < |numbers|)
        invariant 0 <= i && i <= |numbers|
        invariant flag == (exists i1: int, j1: int :: i1 >= 0 && j1 >= 0 && i1 < i && j1 < |numbers| && i1 != j1 && !abs1(numbers[i1] - numbers[j1], threshold))
    {
        var j: int := 0;
        while (j < |numbers|)
            invariant 0 <= i && i < |numbers|
            invariant 0 <= j && j <= |numbers|
            invariant flag == (exists i1: int, j1: int :: i1 >= 0 && j1 >= 0 && ((i1 < i && j1 < |numbers|) || (i1 == i && j1 < j)) && i1 != j1 && !abs1(numbers[i1] - numbers[j1], threshold))
        {
            if (i != j)
            {
                var distance: int := abs(numbers[i] - numbers[j]);
                if (distance < threshold)
                {
                    flag := true;
                }

            }
            j := j + 1;
        }
        i := i + 1;
    }
}