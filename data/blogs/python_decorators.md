# Decorators in python

Decorators in python are really hard to understand. This is a simple guide to using them that is hopefully instructive.

The most fundamental trick to understand them is knowing this:

```python
# given
def decorator(f):
    f._decorated = True
    return f

# this:

def func():
    return
func = decorator(func)

# Is the same as:

@decorator
def func():
    return

```

Put in words, a decorator is a pretty way of modifying a function.
