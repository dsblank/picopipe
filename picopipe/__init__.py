## picopipe
## (c) Douglas Blank
## Apache License 2.0 

import joblib
import random
import inspect

def getsource(code):
    if code.__name__ == "<lambda>":
        return "lambda ...: ..."
    elif hasattr(code, "_source"):
        return code._source
    else:
        try:
            return inspect.getsource(code)
        except Exception:
            return code.__name__

def apply(step, outputs):
    return (step(_input) for _input in outputs)

def pipeline(*steps, name=None):
    def pipe(inputs, n_jobs=None, return_as="generator"):
        if n_jobs in [None, 0]:
            outputs = inputs
            for step in steps:
                if hasattr(step, "_pfilter"):
                    outputs = filter(step, outputs)
                else:
                    outputs = apply(step, outputs)

            if return_as == "list":
                outputs = list(outputs)

            return outputs
        else:
            the_pipeline = pipeline(*steps)
            jobs = (joblib.delayed(the_pipeline)([_input], return_as="list") for _input in inputs)
            results = joblib.Parallel(n_jobs=n_jobs, return_as="generator")(jobs)
            return (result[0] for result in results if len(result) > 0)

    pipe.__pipeline__ = {
        "type": "pipeline",
        "name": name if name else "pipeline",
        "steps": [
            step.__pipeline__ if hasattr(step, "__pipeline__")
            else {
                    "type": "function",
                    "name": step.__name__,
                    "code": getsource(step)
            } for step in steps],
    }
    return pipe

## Pipeline functions:

def to_mermaid(pipeline):
    graph = _to_mermaid_recursive(pipeline.__pipeline__, [0])
    return graph

def _makename(n):
    return f"node{n}"

def _to_mermaid_recursive(pipeline, index):
    if pipeline["type"] == "pipeline":
        steps = pipeline["steps"]
        subgraph = "subgraph {\n"
        names = []
        for step in steps:
            names.append(_makename(index[0]))
            subgraph += f"    {names[-1]}[\"{step['name']}\"]\n"
            index[0] += 1
        subgraph += "}\n"
        if len(steps) <= 1:
            arrows = ""
        else:
            arrows = ""
            for s in range(len(names) - 1):
                arrows += f"{names[s]} --> {names[s+1]}\n"
        subgraph += arrows
        return subgraph
    elif pipeline["type"] == "connection":
        subgraphs = ""
        for sub_pipeline in pipeline["pipelines"]:
            subgraphs += _to_mermaid_recursive(sub_pipeline, index)
        return subgraphs
    else:
        raise Exception(f"unknown type: {pipeline}")

def connect(*pipelines, name=None):
    def connect(inputs, n_jobs=None):
        for pipeline in pipelines:
            inputs = (lambda pipeline=pipeline: pipeline(inputs, n_jobs=n_jobs))()
        return inputs

    connect.__pipeline__ = {
        "type": "connection",
        "name": name if name else "connection",
        "pipelines": [pipeline.__pipeline__ for pipeline in pipelines],
    }

    return connect

## Utility functions:

def step(function, name):
    if function.__name__ == "<lambda>":
        function._source = "lambda ...: ..."
    function.__name__ = name
    return function

## Step functions:

def pfilter(function):
    function._pfilter = True
    return function

@pfilter
def is_not_none(v):
    return v is not None

## Input wrappers:

def limit(inputs, n_limit):
    """
    """
    for count, value in enumerate(inputs):
        yield value
        if count + 1 == n_limit:
            return

def batch(inputs, size):
    """
    """
    _batch = []
    for value in inputs:
        _batch.append(value)
        if (len(_batch) % size) == 0:
            yield tuple(_batch)
            _batch.clear()
    if _batch:
        yield _batch

def sample(inputs, percent):
    """
    """
    return filter(lambda value: random.random() < percent, inputs)
