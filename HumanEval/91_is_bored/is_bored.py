def is_bored(S):
    import re
    sentences = re.split(r'[.?!]\s*', S)
    return sum(sentence[0:2] == 'I ' for sentence in sentences)
def check(is_bored):
    # Check some simple cases
    assert is_bored("Hello world") == 0, "Test 1"
    assert is_bored("The sky is blue. The sun is shining. I love this weather") == 1, "Test 3"
check(is_bored)
