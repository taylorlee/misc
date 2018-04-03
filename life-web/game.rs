use std::collections::{HashMap, HashSet};
use std::ops::Range;
use std::usize::MAX;

// Game Of Life definitions
const SPAWN: u8 = 3;
const LIVING_CONDITIONS: Range<u8> = (2..4);

pub type Idx = (usize, usize);
pub type Board = HashSet<Idx>;
type Abacus = HashMap<Idx, u8>;

const OFF: usize = MAX / 4;

pub fn setup() -> Board {
    let seed = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ];
    let mut board = Board::new();
    for (i, row) in seed.iter().enumerate() {
        for (j, cell) in row.iter().enumerate() {
            if *cell == 1 {
                board.insert((i + OFF, j + OFF));
            }
        }
    }
    return board;
}
pub fn board_slice(board: &Board, x: isize, y: isize) -> bool {
    let rdx = (x + OFF as isize) as usize;
    let cdx = (y + OFF as isize) as usize;
    return board.contains(&(rdx, cdx));
}

pub fn next_generation(board: &Board) -> Board {
    let mut next = Board::new();
    let mut scratchpad = Abacus::new();
    for &(row, col) in board {
        for rdx in row - 1..row + 2 {
            for cdx in col - 1..col + 2 {
                if !(rdx == row && cdx == col) {
                    let neighbor_idx = (rdx, cdx);
                    let value = scratchpad.entry(neighbor_idx).or_insert(0);
                    *value += 1;
                }
            }
        }
    }
    for (&idx, density) in &scratchpad {
        let living = board.contains(&idx);
        if will_have_life(living, *density) {
            next.insert(idx);
        }
    }
    return next;
}

fn will_have_life(living: bool, density: u8) -> bool {
    return if living {
        //LIVING_CONDITIONS.contains(density) // unstable feature
        density >= LIVING_CONDITIONS.start && density < LIVING_CONDITIONS.end
    } else {
        density == SPAWN
    };
}
