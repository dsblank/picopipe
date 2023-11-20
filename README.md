# picopipe
A small pipeline framework built on top of functions

An article describing development and use of picopipe: 
[Towards Data Science: The Worlds Smallest Data Pipeline Framework](https://medium.com/towards-data-science/the-worlds-smallest-data-pipeline-framework-408eaf1a4ce4)

## Installation

```shell
pip install picopipe
```
## Examples

```python
def add1(value):
    return value + 1

def add2(value):
    return value + 2

def add3(value):
    return value + 3

from picopipe import pipeline

p = pipeline(add1, add2, add3)
p([10, 20, 30])
```

See tests for more examples.

## Visualization

```python
with open("pipeline.mmd", "w") as fp:
    fp.write(to_mermaid(p))
```

Mermaid file (renders in github):

```mermaid
flowchart
subgraph pipeline_98e33e0628b546268abb2af5f74e50f1 ["pipeline"]
end
subgraph pipeline_205813c806fd4b37b40309497768f7c1 ["pipeline"]
    node0["identity"]
    node1["is_not_none"]
    node2["identity"]
end
node0 --> node1
node1 --> node2
click node0 console.log "def&#8194;identity(value):<br/>&#8194;&#8194;&#8194;&#8194;return&#8194;value<br/>"
click node1 console.log "@pfilter<br/>def&#8194;is_not_none(v):<br/>&#8194;&#8194;&#8194;&#8194;return&#8194;v&#8194;is&#8194;not&#8194;None<br/>"
click node2 console.log "def&#8194;identity(value):<br/>&#8194;&#8194;&#8194;&#8194;return&#8194;value<br/>"
subgraph pipeline_d2f205ef957a428abbaa208241125819 ["pipeline"]
    node3["add1"]
    node4["[lambda]"]
end
node3 --> node4
click node3 console.log "def&#8194;add1(value):<br/>&#8194;&#8194;&#8194;&#8194;return&#8194;value&#8194;+&#8194;1<br/>"
click node4 console.log "lambda&#8194;...:&#8194;..."
pipeline_98e33e0628b546268abb2af5f74e50f1 --> pipeline_205813c806fd4b37b40309497768f7c1
pipeline_205813c806fd4b37b40309497768f7c1 --> pipeline_d2f205ef957a428abbaa208241125819
```
