Other references:

* [How to make an iterator in Python](https://treyhunner.com/2018/06/how-to-make-an-iterator-in-python/)

## Generator basics (2.1 and 2.2)
---
Consider the following *generator function* used to produce squares:
```python
def gen_squares(max_root):
    for num in range(max_root):
        yield num ** 2
```

This generator function returns a *generator object* (an iterator whose type is `generator`):
```
>>> gen_squares(5)
<generator object gen_squares at 0x10716c3d0>
```

We can get each square using the `next` method:
```
gen_object = gen_squares(5)

>>> next(gen_object)
0
>>> next(gen_object)
1
>>> next(gen_object)
4
```

...or by using a for loop:
```
>>> for num in gen_object:
...     print(num)
...     
9
16
```

The generator is exhausted after the last square is produced:
```
>>> next(gen_object)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
StopIteration
```

When we don't assign the object to a variable and instead call `next` with the function, we get the following:
```
>>> next(gen_squares(5))
0
>>> next(gen_squares(5))
0
>>> next(gen_squares(5))
0
```

!!! note
    The yield statement simultaneously defines an exit point and a re-entry point. 

## Comparing techniques to produce squares
---
### Methods
The `generators.py` file implements three techniques for producing squares:

* 'normal' function that returns a list
* custom class that implements `__iter__` and `__next__`
* simple generator function

### Command line interface
They can be invoked on the command line.  The general form is `$ generators.py program [options]`. 
In this section, we'll use the 'squares' program.  
Defaults:

* function: simple generator
* timing: off
* printing: on
* number of roots: 5

Examples:

* `$ generators.py squares -t -m 100`: time the generator function with 100 roots
* `$ generators.py squares -f non-gen`: execute the non-generator function with 5 roots and print output to console
* `$ generators.py squares -f class -t -m 10`: time the class implementation with 10 roots

### Results
Here are the execution times for 100 roots:

* non-gen: 33.949353146 s
* class: 0.355291014 s
* gen: 0.24595169100000003 s

## Scalable composability (2.3)
---
Consider the following two functions:
```python
def matching_lines_from_file(path, pattern):
    with open(path) as handle:
        for line in handle:
            if pattern in line:
                yield line.rstrip('\n')


def parse_log_records(lines):
    for line in lines:
        level, message = line.split(': ', 1)
        yield {'level': level, 'message': message}
```

They both produce generator objects. They can be used together in a file-processing workflow. 
You can try out these two together on the command line with `$ generators.py log` (the file path and match pattern are 
hard-coded).

The file-processing service (and software in general) can be more easily scaled when functions do only one thing. 
Some roles we might want our functions to take:

* source
* filter
* mapper (transformer or adapter)
* sink

`parse_log_records()` takes the role of mapper, mapping each line of input to an output dictionary.
`matching_lines_from_file()`, however, is playing two roles: source and filter. The functionality would be more 
composable, and thus scalable, if we break it up:

```python
def lines_from_file(path):
    with open(path) as handle:
        for line in handle:
            yield line.rstrip('\n')

def matching_lines(lines, pattern):
    for line in lines:
        if pattern in line:
            yield line
```

Both produce generator objects, but now the source role is played by `lines_from_file()`, and the filter role by 
`matching_lines()`. So now the flow is `lines_from_file()` --> `matching_lines()` --> `parse_log_records()` --> 
\[sink\]. The middle two take a stream as input.

While `parse_log_records()` maps exactly one input to one output, we could also have generator functions that yield 
several outputs from one input or one output from several inputs (see text for examples).  Running 
`$ generators.py house` executes an example of the latter.

Lastly, note that we can change the following function to use `yield from`, which "delegates to a sub-generator":

```python
def  matching_lines_from_file(pattern, path):
    lines = lines_from_file(path)
    matching = matching_lines(lines, pattern)
    for line in matching:
        yield line

def  matching_lines_from_file(pattern, path):
    lines = lines_from_file(path)
    yield from matching_lines(lines, pattern)
```

## Other iterators in Python (2.4)
---

### Dictionaries
Calling `.items()` on a dictionary returns a `dict_items` object, which Python calls a *view*. There is no base view 
type. An object is a dictionary view if it supports the following:

* `len(view)` returns number of items
* `iter(view)` returns an iterator over the k-v pairs
* `(key, value) in view` returns `True` or `False`

Python 3's `.items()` replaces Python 2's `.items()` and `.iteritems()`.

Dictionaries also have `.keys()` and `.values()` methods.

### Others
The built-in `range`, `map`, `filter`, and `zip` all return iterators. See examples in book.

