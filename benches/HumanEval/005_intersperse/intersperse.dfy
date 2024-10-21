
method intersperse(numbers: seq<int>, delimeter: int) returns (res: seq<int>)
ensures |numbers| != 0 ==> |numbers| * 2 - 1 == |res|
ensures |numbers| == 0 ==> |res| == 0
ensures forall i : int :: i >= 0 && i < |res| && i % 2 == 0 ==> res[i] == numbers[i / 2]
ensures forall i : int :: i >= 0 && i < |res| && i % 2 == 1 ==> res[i] == delimeter
{
    res := [];
    if (|numbers| != 0)
    {
        var i : int := 0;
        while (i + 1 < |numbers|)
        invariant 0 <= i && i < |numbers|
        invariant |res| == 2 * i
        invariant forall i1 : int :: i1 >= 0 && i1 < |res| && i1 % 2 == 0 ==> res[i1] == numbers[i1 / 2]
        invariant forall i1 : int :: i1 >= 0 && i1 < |res| && i1 % 2 == 1 ==> res[i1] == delimeter
        {
            res := res + [numbers[i]];
            res := res + [delimeter];
            i := i + 1;
        }
        res := res + [numbers[i]];
    }
}
