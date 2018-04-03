
use std::time::Duration;

use yew;
use yew::html::*;
use yew::services::interval::IntervalService;
use yew::services::Task;

use game::*;

struct Model {
    board: Board,
    clock: u64,
    speed: u8,
    job: Option<Box<Task>>,
    running: bool,
}

enum Msg {
    Step,
    Incr,
    Decr,
    Start,
    Stop,
    Reset,
}

struct Context {
    interval: IntervalService<Msg>,
}

const LEN: usize = 50;
const DIM: usize = LEN*2;

type Row = [bool; DIM];
type Grid = [Row; DIM];

fn new_grid() -> Grid {
    [[false; DIM]; DIM]
}

fn cycle_time(speed: u8) -> Duration {
    Duration::from_millis(500 - 50 * speed as u64)
}

fn do_start(context: &mut Context, model: &mut Model) {
    let handle = context.interval.spawn(cycle_time(model.speed), || Msg::Step);
    model.job = Some(Box::new(handle));
    model.running = true;
}

fn do_stop(model: &mut Model) {
    if let Some(mut task) = model.job.take() {
        task.cancel();
    }
    model.job = None;
    model.running = false;
}

fn restart(context: &mut Context, model: &mut Model) {
    do_stop(model);
    do_start(context, model);
}

fn update(context: &mut Context, model: &mut Model, msg: Msg) {
    match msg {
        Msg::Start => {
            do_start(context, model);
        }
        Msg::Stop => {
            do_stop(model);
        }
        Msg::Reset => {
            model.board = setup();
            model.clock = 0;
        }
        Msg::Step => {
            model.clock += 1;
            model.board = next_generation(&model.board);
        }
        Msg::Incr => {
            if model.speed < 10 {
                model.speed += 1;
            }
            if model.running {
                restart(context, model);
            }
        }
        Msg::Decr => {
            if model.speed > 0 {
                model.speed -= 1;
            }
            if model.running {
                restart(context, model);
            }
        }
    };
}

fn board2grid(board: &Board) -> Grid {
    let mut rows = new_grid();
    for rdx in 0..DIM {
        for cdx in 0..DIM {
            let x = rdx as isize - LEN as isize;
            let y = cdx as isize - LEN as isize;
            rows[rdx][cdx] = board_slice(&board, x, y);
        }
    }
    return rows;
}

fn view(model: &Model) -> Html<Msg> {
    let rows = board2grid(&model.board);
    html! {
        <div>
            <section class="section",>
                <div class="container",>
                    <div class="level",>
                        <div class="level-item",>
                            <h1 class="title",>{ "Game of Life" }</h1>
                        </div>
                    </div>
                </div>
                <div class="level",></div>
                <div class="container",>
                    <div class="level",>
                        <div class="level-item",>
                            <div class=("tags","has-addons"),>
                              <span class="tag",> {"Generation #"}</span>
                              <span class=("tag","is-primary"),> { model.clock } </span>
                            </div>
                        </div>
                    </div>
                    <div class="level",>
                        { if model.running { show_pause() } else { show_start() } }
                    </div>
                    <div class="level",>
                        <div class="level-item",>
                            <div class=("tags","has-addons"),>
                              <span class="tag",> {"SPEED"} </span>
                              <span class=("tag","is-primary"),> { model.speed} </span>
                            </div>
                        </div>
                    </div>
                    <div class="level",>
                        <div class="level-item",>
                            <button class="button", onclick=|_| Msg::Decr,>{ "Slow Down" }</button>
                            <button class="button",  onclick=|_| Msg::Incr,>{ "Speed Up" }</button>
                        </div>
                    </div>
                </div>
                <div class="level",></div>
                <div class="container",>
                    <div class="level",>
                        <div class="level-item",>
                            <table class="grid",>
                                { for rows.iter().map(view_row)  }
                            </table>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    }
}

fn show_start() -> Html<Msg> {
    html! {
        <div class="level-item",>
            <button class="button", onclick=move|_| Msg::Step,>{ "Step" }</button>
            <button class="button", onclick=move|_| Msg::Start,>{ "Start" }</button>
            <button class="button", onclick=move|_| Msg::Reset,>{ "Reset" }</button>
        </div>
    }
}
fn show_pause() -> Html<Msg> {
    html! {
        <div class="level-item",>
            <button class="button", onclick=move|_| Msg::Stop,>{ "Pause" }</button>
        </div>
    }
}

fn view_row(cells: &Row) -> Html<Msg> {
    html! {
        <tr class="row",>
            { for cells.iter().map(view_cell) }
        </tr>
    }
}

fn view_cell(living: &bool) -> Html<Msg> {
    html! {
        <td class=("cell", if *living { "living" } else { "dead" } ),</td>
    }
}

pub fn serve() {
    yew::initialize();
    let mut app = App::new();
    let context = Context {
        interval: IntervalService::new(app.sender()),
    };
    let model = Model {
        board: setup(),
        speed: 5,
        clock: 0,
        job: None,
        running: false,
    };
    app.mount(context, model, update, view);
    yew::run_loop();
}
