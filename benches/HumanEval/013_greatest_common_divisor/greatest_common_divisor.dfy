// recursive version should be more promising

method greatest_common_divisor(a: int, b: int) returns (gcd: int)
    requires a != 0 || b != 0 
    ensures gcd != 0 
{
    var x := a;
    var y := b;
    while (y != 0)
        invariant x != 0 || y != 0
    {
        var temp := y;
        y := x % y;
        x := temp;
    }
    gcd := x;
}