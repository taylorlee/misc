## Motivation
When I try to understand the Y-Combinator, it often feels like this:
```
Wikipedia: Y = λf.(λx.x x) (λx.f (x x))
Me: Wat.
```
Lambda calculus can make my head hurt, but code refactorings seem more approachable. As such, I really like Peter Krumins' [derivation of the Y-Combinator](http://www.catonmat.net/blog/derivation-of-ycombinator/).
I thought it would be fun to try something similar, but using the nice lambda syntax of ES6.

## Background
Many explanations of Turing Completeness portray the notion that generic computation is dependent on unbounded loops. (Eg [BlooP and FlooP](https://en.wikipedia.org/wiki/BlooP_and_FlooP) )
This gives the impression that languages supporting unbounded loops are Turing Complete, while all others are not.
This is a false notion, since recursion and iteration have equal expressive power.
Thus, languages with recursion can be turing complete without supporting loops at all.
What if a language didn't explicitly support either iteration or recursion?

Let's see an example of what that might look like.

## primitive ES6
Let's imagine we have a language alot like ES6, but missing the following keywords:
```js
for
while
function
```
We'll have to get rid of hoisting too, to fully prevent named recursion.
We'll assume we don't have access to ```forEach``` and ```map``` either.
Let's call our primitive ES6 "p6".

Is p6 Turing complete? 
To disqualify ridiculous systems like JSfuck, let's also assume that basic math operators ```(+,-,*,/)``` throw type errors when the operands have different prototypes.

Whew. Seems like we had to rip alot out of JS.
So have we made p6 non-turing complete yet?

## Length of a list
For the sake of example, let's imagine that JS objects don't have a ```length``` property either.

How can we calculate the length of a list?
(imagine a linked list instead of a JS Array)

```js
// This won't work in our language p6 due to lack of hoisting!
len = list =>  l[0] === undefined ? 0 : 1 + len(list.slice(1))
// length hasn't been defined yet...
```

## Trying to sneak around the edges
Using a Test Driven Development mentality, I'll try to get the correct values
for the length of each of the following lists:
```js
// test data
example_lists = [ [], [1], [1,2], [1,2,3], [1,2,3,4] ]
```

Let's start with the most basic example: test if a list is empty.
```js
lenLessThan1 = l => l[0] === undefined ? 0 : 1 
> example_lists.map(x=>lenLessThan1(x))
[ 0, 1, 1, 1, 1 ] 
```
So far so good. Not very helpful.... but we can build on that foundation:
```js
lenLessThan2 = l => l[0] === undefined ? 0 : 1 + lenLessThan1(l.slice(1))
lenLessThan3 = l => l[0] === undefined ? 0 : 1 + lenLessThan2(l.slice(1))

> example_lists.map(x=>lenLessThan2(x))
[ 0, 1, 2, 2, 2 ] 
> example_lists.map(x=>lenLessThan3(x))
[ 0, 1, 2, 3, 3 ] 
```
Yay! We can tell the difference between lists of 0, 1, 2, and 3-or-more elements!
A small victory.
Intuition should tell us that this strategy isn't extensible to arbitrary lists.

Since ```lenLessThan3``` looks alot like ```lenLessThan2```, we can try to refactor them.

```js
makeLen = prevLen => l => l[0] === undefined ? 0 : 1 + prevLen(l.slice(1))
// now we define 
lenLessThan2 = makeLen(lenLessThan1)
lenLessThan3 = makeLen(makeLen(lenLessThan1))
```
Okay, so this is slightly more abstract. But it doesn't get us away from needing to
make an infinite amount of calls to ```makeLen``` in order to support arbitrary
input lists. It feels like we need a way to pass ```makeLen``` to itself.

But we can't to this (yet), because ```makeLen``` takes a function as its first 
argument, while ```prevLen``` takes a list as its first argument.


## The Trick
So here is the trick: we'll change ```prevLen``` to ```prevRecLen```, and have it
also take a function as its first argument.

```js
recLen = prevRecLen => l => l[0] === undefined ? 0 : 1 + prevRecLen(prevRecLen)(l.slice(1))
```
See how close this is to ```makeLen``` ?
But now ```recLen``` and ```prevRecLen``` take the same type of argument,
allowing this:
```js
len = recLen(recLen)
> example_lists.map(x=>len(x))
[ 0, 1, 2, 3, 4 ] 
//whoah! we can handle arbitrary lists
```

Yay! This might seems like a trivial example, but remember that we just forced
recursion into a language ("p6") that was designed explicitly to remove unbounded
loops and recursion.

## Refactors
I promised some refactors, so let's get started. 
The goal is to split our implementation of ```len``` into two parts
1. makeLen (non-recursive, just knows how to compute length)
2. some kind of function combiner that makes other funtions recursive

Refactors to the rescue:
```js
// define recLen by delegation to makeLen
recLen = prevRecLen => l => l[0] === undefined ? 0 : 1 + prevRecLen(prevRecLen)(l.slice(1))
// becomes:
makeLen = prevLen => l => l[0] === undefined ? 0 : 1 + prevLen(l.slice(1))
recLen = prevRecLen => makeLen(l => prevRecLen(prevRecLen)(l))

// let len refer to recLen only once:
len = recLen(recLen)
// becomes:
len = (x => x(x))(recLen)

// combine these two definitions by replacing recLen with its definition inline:
len = (x => x(x))(prevRecLen => makeLen(l => prevRecLen(prevRecLen)(l)))

// pull makeLen out so it can be passed as an argument
len = (maker => 
    (x => x(x))(prevRecLen => maker(l => prevRecLen(prevRecLen)(l)))
)(makeLen)

// and pull these concept apart one final time:
function_combiner = maker => 
    (x => x(x))(prevRecLen => maker(l => prevRecLen(prevRecLen)(l)))
    
len = funcion_combiner(makeLen)
```

## Cleanup
Whew! Every step should make sense, but by now ```function_combiner``` has
accumulated strange variable names and is hard to understand. Since the 
variables are generic now, we can apply the following renaming:
```
'maker' -> 'f' (whatever function would like to become recursive)
'prevRecLen' -> 'x' (safe rename, since it's in a distict scope from the other 'x')
'l' -> 'a' (standing for list -> argument)
'function_combiner' -> 'Y' (as in combinator!)
```
Now we get:
```js
Y = f => (x => x(x))(x => f(a => x(x)(a)))
len = Y(makeLen)
```
Wow! Oh hey, it's the Y-Combinator! Who knew.

Just to make sure this isn't a fluke, we can use this combinator to build 
another, slightly more complex, recursive function.

```js
// fibonnaci function from lambdas
makeFib = _fib => n =>
    (n < 2)
    ? 1
    : _fib(n-1) + _fib(n-2)
    
fib = Y(makeFib)
> [0,1,2,3,4,5,6].map(fib)
[ 1, 1, 2, 3, 5, 8, 13 ]
```
Nice! Exactly what we should expect.

## Conclusion
So this technique lets us force recursion by only using anonymous functions.
Let's loop back to what I said in the beginning about Turing-Completeness.

Here's a hand-wavy non-rigorous proof:
 ```
  anonymous functions permit the construction of fixed point combinators
  fixed point combinators allow implicit recursion
  recursion is equivalent to unbounded loops
  unbounded loops provice turing complete computation
  ```

This is why people sometimes call lambda calculus the simplest turing-complete model of computation.

I hope you enjoyed this and I encourage you to play with some fixed point combinators yourself!
(there are in fact infinitely many of them, the Y-Combinator is just one example)

## Footnotes:
1. Why does our definition of the YC have an 'a' in it? The lambda calculus definition
from Wikipedia doesn't have that. It's because javascript isn't lambda calculus, 
we need a method to make sure our argument ('a') gets passed along correctly.
You can compare this definition to the final definition in Peter Krumins' post 
to see the similarity.
