from verified_cogen.tools import compare_errors


def test_compare_errors1():
    err1: str = "Verification timed out"
    err2: str = "Verification timed out"
    assert compare_errors(err1, err2)

def test_compare_errors2():
    err1: str = "Verification timed out"
    err2: str = """\
        Translation failed
    Not supported: (0 <= d_6_i_ <= len(l))
        (/home/aleksandr/verified-cogen/log_tries/humaneval-nagini/040-triples-sum-to-zero.1.py@19.18)"""
    assert not compare_errors(err1, err2)

def test_compare_errors3():
    err1: str = """\
        Translation failed
    Type error: invalid syntax (/home/aleksandr/verified-cogen/log_tries/humaneval-nagini/042-incr-list.2.py@18.0)"""
    err2: str = """\
        Translation failed
    Type error: invalid syntax (/home/aleksandr/verified-cogen/log_tries/humaneval-nagini/042-incr-list.3.py@18.0)"""
    assert compare_errors(err1, err2)

def test_compare_errors4():
    err1: str = """\
        Translation failed
    Type error: invalid syntax (/home/aleksandr/verified-cogen/log_tries/humaneval-nagini/042-incr-list.1.py@19.0)"""
    err2: str = """\
        Translation failed
    Type error: invalid syntax (/home/aleksandr/verified-cogen/log_tries/humaneval-nagini/042-incr-list.3.py@18.0)"""
    assert not compare_errors(err1, err2)

def test_compare_errors5():
    err1: str = """\
        Verification failed
    Errors:
    Loop invariant might not be preserved. Assertion (s == psum(0, d_2_i_, numbers)) might not hold. (008-sum-product.3.py@32.18--32.47)
    Verification took 9.04 seconds."""
    err2: str = """\
        Verification failed
    Errors:
    Loop invariant might not be preserved. Assertion (s == psum(0, d_2_i_, numbers)) might not hold. (008-sum-product.4.py@32.18--32.47)
    Verification took 13.72 seconds."""
    assert compare_errors(err1, err2)