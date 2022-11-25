# Day 10, Advent of Code 2021

Let's figure out how to turn [Day 10, Advent of Code 2021](https://adventofcode.com/2021/day/10) into a task for an artificial neural network.


## Part 1

For Day 10, This task is to identify syntax errors in a grammar consisting of
nested parenthesis/brackets.  Only 8 symbols are used: `()`, `[]`, `{}`, `<>`

Here are some *valid* lines in the grammar.
```
<>
[[]]({}<>)
()
{{}()<<>>}
```

Here are some *invalid* lines in the grammar.
```
<
[[]]({}>)
(]
{{}()<>>}
```
