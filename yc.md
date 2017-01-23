# FIRST DRAFT: NEEDS REVISION!!!


## Motivation

Lambda calculus makes my head hurt, but code refactorings are my bread and butter. As such, I really like Peter Krumins' [derivation of the Y-Combinator](http://www.catonmat.net/blog/derivation-of-ycombinator/).
I thought it would be fun to try something similar, but using the nice lambda syntax of ES6.

## Background
Many explanations of Turing Completeness portray the notion that generic computation is dependent on unbounded loops.
This gives the impression that languages supporting unbounded loops are Turing Comlete, while all others are not.
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

## getting the length of an array
For the sake of example, let's imagine that JS objects don't have a ```length``` property either.

How can we calculate the length of an array?

```js
// This won't work in p6 due to lack of hoisting!
let length = array => {
    if (array[0] === undefined) {
        return 0
    } else {
        return 1 + length(array.slice(1))
    }   
}
// length hasn't been defined yet...
```

## Trying to sneak around the edges
Let's start with the most basic example: test if an array is empty.
```js
let zeroIfEmpty = array => {
    if (array[0] === undefined) {
        return 0
    } else {
        return 1
    }
}
```
And then build on that foundation:
```js
let length = array => {
    if (array[0] === undefined) {
        return 0
    } else {
        return 1 + zeroIfEmpty(array.slice(1))
    }
}
```
Yay! We can tell the difference between arrays of 0, 1, and 2-or-more elements!
A small victory.
Intuition should tell us that this strategy isn't extensible to unbounded arrays.


What if we try to copy the pattern inline?

# TODO: finish derivation
