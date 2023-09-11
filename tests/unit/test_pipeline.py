from picopipe import pipeline, pfilter, limit, batch, sample, is_not_none, to_mermaid, connect

def add1(value):
    return value + 1

def add2(value):
    return value + 2

def add3(value):
    return value + 3

def identity(value):
    return value

def test_empty_pipe():
    p = pipeline()
    result = list(p([1, 2, 3]))
    assert result == [1, 2, 3]

def test_function1_list():
    assert [x for x in pipeline(add1)([1, 2, 3])] == [2, 3, 4], "input is list"

def test_function1_expr():
    assert [x for x in pipeline(add1)(x for x in [1, 2, 3])] == [2, 3, 4], "input is generator"

def test_function2_list():
    assert [x for x in pipeline(add1, add1)([1, 2, 3])] == [3, 4, 5], "input is list, sequence"

def test_function2_expr():
    assert [x for x in pipeline(add1, add1)(x for x in [1, 2, 3])] == [3, 4, 5], "input is generator, sequence"

def test_identity_list():
    assert [x for x in pipeline(identity)([1, 2, 3])] == [1, 2, 3], "input is list"

def test_identity_expr():
    assert [x for x in pipeline(identity)(x for x in [1, 2, 3])] == [1, 2, 3], "input is generator"

def test_identity_filter_input_list():
    assert [x for x in pipeline()(filter(lambda v: v % 2 == 0, [1, 2, 3, 4, 5]))] == [2, 4], "filter input, list"

def test_identity_filter_input_expr():
    assert [x for x in pipeline()(filter(lambda v: v % 2 == 0, (x for x in [1, 2, 3, 4, 5])))] == [2, 4], "filter input, generator"

def test_function1_filter_input_list():
    assert [x for x in pipeline(add1)(filter(lambda value: value % 2 == 0, [1, 2, 3, 4, 5]))] == [3, 5], "filter input, list"

def test_function1_filter_input_expr():
    assert [x for x in pipeline(add1)(filter(lambda value: value % 2 == 0, (x for x in [1, 2, 3, 4, 5])))] == [3, 5], "filter input, generator"

def test_function1_pfilter_list():
    assert [x for x in pipeline(add1, pfilter(lambda v: v % 2 == 0))([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])] == [2, 4, 6, 8, 10], "pfilter, input generator"

def test_function1_pfilter_expr():
    assert [x for x in pipeline(add1, pfilter(lambda v: v % 2 == 0))(x for x in range(10))] == [2, 4, 6, 8, 10], "pfilter, input generator"

def test_limit_list():
    [x for x in pipeline(identity, identity, identity)(limit([1, 2, 3, 4], 2))] == [1, 2]

def test_limit_expr():
    [x for x in pipeline(identity, identity, identity)(limit((x for x in [1, 2, 3, 4]), 2))] == [1, 2]

def test_batch_list():
    [x for x in pipeline(identity, identity, identity)(batch([1, 2, 3, 4, 5], 2))] == [(1, 2), (3, 4), (5,)]

def test_batch_expr():
    [x for x in pipeline(identity, identity, identity)(batch((x for x in [1, 2, 3, 4, 5]), 2))] == [(1, 2), (3, 4), (5,)]

def test_sample():
    results = [x for x in pipeline(identity, identity, identity)(sample(range(100), 0.5))]
    assert 35 < len(results) < 65

def test_is_not_null():
    results = [x for x in pipeline(identity, is_not_none, identity)([1, None, 2, None, 3])]
    assert results == [1, 2, 3]

def test_mermaid1():
    p = pipeline(identity, is_not_none, identity)
    assert to_mermaid(p) != None

def test_mermaid2():
    p = pipeline(add1, pfilter(lambda v: v % 2 == 0))
    assert to_mermaid(p) != None

def test_mermaid3():
    p = pipeline()
    assert to_mermaid(p) != None

def test_connect():
    p1 = pipeline(identity, is_not_none, identity)
    p2 = pipeline(add1, pfilter(lambda v: v % 2 == 0))

    p3 = connect(p1, p2)
    results = [x for x in p3([1, 2, 3, None, 4, 5, 6])]
    assert results == [2, 4, 6]
