## picopipe
## (c) Douglas Blank
## Apache License 2.0 

import joblib
import typing

def pipeline(*steps, n_jobs=1):
    """
    """
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
        return pipe
    else:
        def pipe(input):
            if isinstance(input, (typing.Generator, typing.Iterator)):
                inputs = map(steps[0], input)
            else:
                inputs = steps[0](input)
            jobs = (joblib.delayed(pipeline(*steps[1:]))(_input)
                    for _input in inputs)
            return [results for results in
                    joblib.Parallel(n_jobs=n_jobs)(jobs)]
    return pipe

## Step wrappers

def limit(step, n_limit):
    """
    """
    def wrapper(inputs):
        for count, value in enumerate(step(inputs)):
            yield value
            if count + 1 >= n_limit:
                return
    return wrapper

def filter(step, function):
    """
    """
    def wrapper(inputs):
        for value in step(inputs):
            if function(value):
                yield value
    return wrapper
