use std::thread::sleep;
use std::time::Duration;
use std::ops::Range;
use game::*;

// INTERACTIVE PARAMS
const DURATION: u64 = 100;

// Game Of Life definitions
const CELL: char = 'O';

// VIEWING WINDOW CALC
const VIEW: Range<isize> = (-10..11);

pub fn serve() {
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
