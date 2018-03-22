
## First thoughts with rust:

For a while I've been intrigued by rust and the potential it seems to hold for offering efficiency without compromising productivity.

As a predominantly python programmer, I'm intrigued by eliminating dynamic typing errors without sacrificing the use of convenient high level abstractions.

Since my first main language was C++, I'm intrigued by memory safety without a garbage collector.

I've been watching the development of the language and ecosystem, but never seriously tried to build anything using it other than hello-world, etc.

As a first test in developing with rust, I decided to pick a problem that would be simple enough to implement a functioning first version quickly, yet complex enough to yield multiple orders of magnitude in efficiency gains through optimization tweaks.

To that goal, I picked [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), as the rules are extremely simple, yet some initial configurations can balloon up in computational complexity.

## Step one: copy-paste example from internet ;)
```rust
fn main() {
    // The statements here will be executed when the compiled binary is called
    // Print text to the console
    println!("Hello World!");
}
```

## Step two: iterate!
I decided to run the simulation by printing to the console, with spaces denoting empty cells and "0"s denoting living cells.

```rust
fn main() {
    println!("Conway's Game of Life:");
    println!("");
    println!(" 0 ");
    println!("0 0");
    println!(" 0 ");
}
```

## Step three: Game of Life
I started with a simple array of integers to represent the grid.

```rust
const DIM: usize = 10;

type Row = [usize; DIM];
type Grid = [Row; DIM];

fn clean_grid() -> Grid {
    [[0; DIM]; DIM]
}

```
From there, I could embed a starting configuration within the larger grid.
I picked the [Acorn config](http://www.conwaylife.com/wiki/Acorn) since it starts small but blooms on for several thousand iterations.
```rust
fn setup() -> Grid {
    let mut grid = clean_grid();
    let seed = [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0],
        [0,0,1,1,0,0,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
    ];
    for i in 0..seed.len() {
        for j in 0..seed.len(){
            grid[i][j] = seed[i][j];
        }
    }
    return grid;
}
```
From there is was relatively straightforward to write functions to print the grid and apply the cellular automata logic to compute the next generation. (grid_print and cell_lives omitted for brevity)

```rust
fn main() {
    let mut rows = setup();
    for i in 0.. {
        grid_print(rows);
        rows = next_generation(rows);
    }
}

fn next_generation(grid: Grid) -> Grid {
    let mut next = clean_grid();
    let size = grid.len();
    for row_idx in 0..size {
        for col_idx in 0..size {
            if cell_lives(row_idx, col_idx, grid) {
                next[row_idx][col_idx] = 1;
            }
        }
    }
    return next
}
```
And that worked!
First three generations:
 - - - - - - - - - -
-                    -
-                    -
-      O             -
-          O         -
-    O O     O O O   -
-                    -
-                    -
-                    -
-                    -
-                    -
 - - - - - - - - - -
 - - - - - - - - - -
-                    -
-                    -
-                    -
-    O O O   O O     -
-            O O     -
-              O     -
-                    -
-                    -
-                    -
-                    -
 - - - - - - - - - -
 - - - - - - - - - -
-                    -
-                    -
-      O             -
-      O   O O O     -
-      O   O     O   -
-            O O     -
-                    -
-                    -
-                    -
-                    -
 - - - - - - - - - -

## Step four: profile
Always profile before optimization!

Annoyance #1: cargo has a ```profile``` command, but it's currently in nightly and I'm on stable.
Solution: simple timer:
```rust
fn main() {
    let mut rows = setup();
    let start = Instant::now();
    for i in 0.. {
        rows = gol(rows);
        if i == BENCH {
            let now = start.elapsed();
            let result = now.as_secs() as f64 + now.subsec_nanos() as f64 * 1e-9;
            println!("{}", result);
            return;
        }
    }
}
```

## Step five: optimize 
A really easy optimization was to shrink the grid's memory footprint by switching from pointer-sized unigned integer to boolean.
```diff
-type Row = [usize; DIM];
+type Row = [bool; DIM];
 type Grid = [Row; DIM];
  
 fn clean_grid() -> Grid {
-    [[0; DIM]; DIM]
+    [[false; DIM]; DIM]
}
```
And that speed up the simulation by about 10X!

I experimented with a few other optimizations, but it became clear that the grid approach was flawed for two reasons:

1. computing next_generation is inevitable O(NxN), which gets prohibitively expensive at large N
2. some configurations grow indefinitely, so any border limitation won't be an accurate simulation
(for example, Acorn emits [gliders](https://en.wikipedia.org/wiki/Glider_(Conway%27s_Life))
 - - - - - -
-            -
-    O       -
-      O     -
-  O O O     -
-            -
 - - - - - -
which propagate diagonally forever)

From Arrays to HashSets:

My solution to removing the bounding nature of the grid was to separate the idea of the cell space and the view pane.
The new game board would consist of the set of all coordinates currently living.
The print representiation would iterate over the desired window coordinates, printing cells if those coordinate were part of the currently living set.
This has the nice property of reducing the computational complexity to O(number_currently_living_cells).

```rust
use std::usize::MAX;

const DIM : usize = MAX;
const OFFSET: usize = DIM / 2;
const VIEW: (usize, usize) = (OFFSET - VIEWSIZE/2, OFFSET+VIEWSIZE/2);
```

Note: The simulation *is* still bounded, but MAX (9223372036854775807 on my computer) is more than enough for my purposes.

Correspondingly, the simulating is not waay faster. About a 100X speedup at the 1000-generation benchmark, and even more for higher grid sizes.

## Conclusions:
I made some other optimizations, and identified some that I never introduced.
But the main point was to play with rust, so I'll comment on that now.

Overall I was very satisfied with the language and tooling.
I've worked offline for the majority of this project, so the builtin docs have been crucial: 
```
rustup doc --std
rustup doc --book
```

The borrow checker took a little getting used to, but the compiler errors were extremely helpful.
I was usually able to take the compiler's suggested change to fix borrowing errors.

The main complaint I have so far is the number of features currently on the nightly release. (I prefer to stay on stable).
At the time of writing some of these are:

* std::collections::Range (in particular the ```contains``` method)
* benchmarking
* rustfmt
* incremental compilation

The good news is that I expect these to be stabilized before long!

More good news is that rust looks well positioned to support two use cases I'm excited about:
* replacing critical path sections of python programs through CFFI
* building clientside web apps by compiling to wasm

Hopefully I'll take a crack at both of these soon and post the results here!
