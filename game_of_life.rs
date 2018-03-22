#![allow(dead_code)]

use std::collections::{HashSet, HashMap};
use std::thread::sleep;
use std::time::{Duration, Instant};
use std::usize::MAX;
use std::ops::Range;

// INTERACTIVE PARAMS
// slow
//const VIEWSIZE       : usize    = 20   ;
//const DURATION       : u64      = 2000 ;

// med
const VIEWSIZE       : usize    = 100   ;
const DURATION       : u64      = 100   ;

// fast
//const VIEWSIZE         : usize    = 200   ;
//const DURATION         : u64      = 10    ;

// benchmarking params
const CYCLES           : usize = 1000 ;

// Game Of Life definitions
const CELL              : char      = 'O'   ;
const SPAWN             : u8        = 3     ;
const LIVING_CONDITIONS : Range<u8> = (2..4);

type Board = HashSet<(usize, usize)>;
type Abacus = HashMap<(usize, usize), u8>;

// VIEWING WINDOW CALC 
const DIM : usize = MAX;
const OFFSET: usize = DIM / 2;
const VIEW: Range<usize> = (OFFSET-VIEWSIZE/2..1+OFFSET+VIEWSIZE/2);

fn setup() -> Board {
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
    let mut board = Board::new();
    for (i, row) in seed.iter().enumerate() {
        for (j, cell) in row.iter().enumerate() {
            if *cell == 1 {
                board.insert((i+OFFSET, j+OFFSET));
            }
        }
    }
    return board;
}

fn main() {
    benchmark();
    //interactive();
}

fn benchmark() {
    size_after_iterations(CYCLES);
}

fn interactive() {
    let mut board = setup();

    for i in 0.. {
        print!("{}[2J", 27 as char); // clear screen
        let num_cells = board.len();
        println!("{} iterations arrived at {} cells", i, num_cells);
        print_board(&board);
        sleep(Duration::from_millis(DURATION));
        board = next_generation(&board);
    }
}

fn size_after_iterations(cycles: usize) -> usize {
    let mut board = setup();
    let start = Instant::now();
    for _ in 0..cycles {
        board = next_generation(&board);
    }
    let now = start.elapsed();
    let result = now.as_secs() as f64 + now.subsec_nanos() as f64 * 1e-9;
    let num_cells = board.len();
    println!("{} iterations arrived at {} cells", cycles, num_cells);
    println!("Took {}", result);
    return num_cells;
}

fn next_generation(board: &Board) -> Board {
    let mut next = Board::new();
    let mut scratchpad = Abacus::new();
    for &(row, col) in board {
        for rdx in row-1..row+2 {
            for cdx in col-1..col+2 {
                if ! (rdx == row && cdx == col) {
                    let neighbor_idx = (rdx, cdx);
                    let value = scratchpad.entry(neighbor_idx).or_insert(0);
                    *value += 1;
                }
            }
        }
    }
    for (&idx, density) in &scratchpad {
        let living = board.contains(&idx);
        if will_have_life(living, *density)  {
            next.insert(idx);
        }
    }
    return next;
}

fn will_have_life(living: bool, density: u8) -> bool {
    return if living {
        density >= LIVING_CONDITIONS.start && density < LIVING_CONDITIONS.end
        //LIVING_CONDITIONS.contains(density) // unstable feature
    } else {
        density == SPAWN
    }
}

fn draw_line() {
    for _ in VIEW {
        print!("--");
    }
    println!("");
}

fn print_board(board: &Board) {
    draw_line();
    for row in VIEW {
        print!("-");
        for col in VIEW {
            if board.contains(&(row, col)) {
                print!("{} ", CELL);
            } else {
                print!("  ");
            }
        }
        print!("-\n");
    }
    draw_line();
}

#[cfg(test)]
mod tests {
    use size_after_iterations;

    #[test]
    fn setup() {
        assert_eq!(size_after_iterations(0), 7);
    }

    #[test]
    fn short() {
        assert_eq!(size_after_iterations(10), 30);
    }

    #[test]
    fn med() {
        assert_eq!(size_after_iterations(100), 76);
    }

    #[test]
    fn long() {
        assert_eq!(size_after_iterations(1000), 457);
    }
}
