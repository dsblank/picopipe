## picopipe
## (c) Douglas Blank
## Apache License 2.0 

import joblib
import typing
import random
import inspect

def pipeline(*steps, n_jobs=1):
    if n_jobs == 1:
        def pipe(input):
            output = None
            for step in steps:
                if isinstance(input, (typing.Generator, typing.Iterator)):
                    output = map(step, input)
                else:
                    output = step(input)
                input = output
            return output
    else:
        def pipe(input):
            if isinstance(input, (typing.Generator, typing.Iterator)):
                inputs = map(steps[0], input)
            else:
                inputs = steps[0](input)
            jobs = (joblib.delayed(pipeline(*steps[1:]))(_input) for _input in inputs)
            return joblib.Parallel(n_jobs=n_jobs, return_as="generator")(jobs)

    pipe.__pipeline__ = {
        "type": "pipeline",
        "steps": [step.__pipeline__ if hasattr(step, "__pipeline__")
                  else {
                          "type": "function",
                          "name": step.__name__,
                          "code": inspect.getsource(step)
                  } for step in steps],
        "n_jobs": n_jobs
    }
    return pipe

## Step wrappers

def limit(step, n_limit):
    """
    """
    def limit(inputs):
        for count, value in enumerate(step(inputs)):
            yield value
            if count + 1 >= n_limit:
                return
    return limit

def filter(step, function):
    """
    A step wrapper that filters the data.

    Args:
        step: a function
    """
    def filter(inputs):
        for value in step(inputs):
            if function(value):
                yield value
    return filter


def sample(step, percent):
    """
    A step wrapper that selects about percent of items.

    Args:
        step: a function
        percent: a number between 0 and 1
    """
    return filter(
        step1, 
        lambda value: random.random() < percent
    )
