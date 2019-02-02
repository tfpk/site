~~~
md_name = "python_decorators"
name = "Understanding Python Decorators"
desc = "Decorators are a powerful python tool to improve your code... Here's how to use them."
image = "images/decorator_code.jpg"
~~~
# Decorators in python

Decorators in python are really hard to understand. This is a simple guide to using them that is hopefully instructive.

The most fundamental trick to understand them is knowing this:

    # given
    def decorator(f):
        # do things
        return f

    # this:

    def func():
        return
    func = decorator(func)

    # Is the same as:

    @decorator
    def func():
        return


Put in words, a decorator is a way of modifying how a function is declared.

It has two essential components to it:

 - It runs the code inside the decorator
 - It replaces the function given with whatever value the decorator returns.

There are three usecases that come as a result of this:

## 1) Performing an action once, when a function is declared

If you want to specify that something happens when a function is declared, the decorator is the right way to do it.

The best use-case is if you're "registering" functions. For instance, say you want to make a list of functions that get run by a single function, you could do the following:

    registered_functions = []
    def register(f):
        registered_functions.append(f)
        return f

    @register
    def print_1():
        print(1)

    @register
    def print_2():
        print(2)

    @register
    def print_3():
        print(3)

    def run_registered_functions():
        for func in registered_functions:
            func()


    >>> run_registered_functions()
    1
    2
    3

This is contrived, obviously, but I have previously used this for things like:

 - When I'm writing a module that people can import from, you can use this to choose which functions can be imported with `from my_module import *`
 - When I'm writing tests with [pytest](pytest.org), you use decorators to mark tests that should be skipped.

## 2) Modifying the behaviour of a function.

Because you can change what function is returned, you can modify how a function works with decorators. The simplest example of this is:

    def new_function():
        print(2)

    def decorator(f):
        return new_function

    @decorator
    def original_function():
        print(1)


    >>> original_function():
    2

See how even though I'm calling `original_function`, it's actually executing `new_function`, since the decorator returned that instead.

This isn't particularly useful. It's much better to "wrap" the function you're given:

    def decorator(f):
        def wrapper(*args, **kwargs):
            # note, this wrapper will work with any function
            # since it takes any arguments
            print("about to call this function")
            return_value = f(*args, **kwargs)
            if return_value is None:
                print("function did not return anything")
            else:
                print("function returned " + return_value)
        return wrapper
            
    @decorator
    def just_return(value):
        return value


    >>> just_return(None)
    about to call this function
    function did not return anything
    
    >>> just_return(2)
    about to call this function
    function returned 2

This is much more useful. You can do things like:

 - Validate that a function returns something. Or that it returns a particular value (like, that it returns an integer)
 - Modify the return value. The best example of this is to make it so that a function is only run once, and any following calls to it return the same value.

 ## 3) Adding arguments to modify a function

 One of the best perks of decorators is a feature that hasn't been demonstrated in this article: they can take arguments.
 That works like this:

    def register(argument):
        def decorator(f):
            print("function decorated with argument: " + argument)
            return f
        return decorator

    @register('the_argument')
    def my_func():
        return


    >>> my_func()
    function decorated with argument the_argument

An example of where this is useful is when writing a web server. You might write a function that describes a particular page,
and then register it with a decorator that gives its address on the server.

# A note on wrappers

When wrapping a function, since a new function is returned, it loses the information about the function it wrapped.
This includes things like the function's name (which can be accessed with `function.__name__`, but might say `wrapper` rather than `my_function_name`).

You can restore this by using the `functools.wraps` decorator on the wrapper function.
