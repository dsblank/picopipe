## picopipe
## (c) Douglas Blank
## Apache License 2.0 

import joblib
import typing
import random
import inspect

def getsource(code):
    try:
        return inspect.getsource(code)
    except Exception:
        return code.__name__

def pipeline(*steps, n_jobs=None, return_as="generator"):
    if n_jobs is None:
        def pipe(inputs):
            outputs = inputs
            for step in steps:
                if hasattr(step, "_is_a_filter"):
                    outputs = filter(step, outputs)
                else:
                    outputs = (lambda step=step: (step(_input) for _input in outputs))()

            if return_as == "list":
                outputs = list(outputs)

            return outputs

        return pipe
    else:
        def pipe(inputs):
            jobs = (joblib.delayed(pipeline(*steps, return_as="list"))([_input]) for _input in inputs)
            return (results[0] for results in joblib.Parallel(n_jobs=n_jobs, return_as="generator")(jobs) if len(results) > 0)

    pipe.__pipeline__ = {
        "type": "pipeline",
        "steps": [step.__pipeline__ if hasattr(step, "__pipeline__")
                  else {
                          "type": "function",
                          "name": step.__name__,
                          "code": getsource(step)
                  } for step in steps],
        "n_jobs": n_jobs
    }
    return pipe

## Step functions:

def is_a_filter(function):
    function._is_a_filter = True
    return function

@is_a_filter
def is_not_null(v):
    return v is not None

## Input wrappers:

def limit(inputs, n_limit):
    """
    """
    for count, value in enumerate(inputs):
        yield value
        if count + 1 == n_limit:
            return

def sample(inputs, percent):
    """
    """
    return filter(
        lambda value: random.random() < percent,
        inputs, 
    )
