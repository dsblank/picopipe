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

def pipeline(*steps, n_jobs=None, pfilter=None, return_as="generator"):
    if n_jobs is None:
        def pipe(inputs):
            output = None
            for step in steps:
                if return_as == "generator":
                    inputs = (step(input) for input in inputs)
                else: # joblib doesn't like generators
                    inputs = [step(input) for input in inputs]
                        
            return inputs
        return pipe
    else:
        def pipe(inputs):
            jobs = (joblib.delayed(pipeline(*steps, return_as="list"))([_input]) for _input in inputs)
            return (x[0] for x in joblib.Parallel(n_jobs=n_jobs, return_as="generator")(jobs))

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
