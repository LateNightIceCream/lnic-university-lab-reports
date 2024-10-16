use ndarray;
use csv;

mod msd;
use msd::{MSDParameters, MSDResult};

const DAMPING_MIN: f32 = 800.0;
const DAMPING_MAX: f32 = 1200.0;

const T_START: f32 = 0.0;
const T_END: f32 = 2.0;
const STEP_WIDTH: f32 = 0.01;

const NUM_RUNS: usize = 2000000;


fn run_msd_mc(params: &MSDParameters) -> MSDResult {
    let my_param = params.with_random_damping(DAMPING_MIN, DAMPING_MAX);
    let result = msd::solve_msd_trajectory(&my_param, T_START, T_END, STEP_WIDTH);
    result
}

fn run_all_msd(params: &MSDParameters) -> MSDResult {

    let mut total_result = run_msd_mc(params);

    for i in 1..NUM_RUNS {
        let result = run_msd_mc(params);
        total_result.states = total_result.states + result.states;
    }

    total_result.states = total_result.states / (NUM_RUNS as f32);

    total_result
}



fn main() {

    const BASE_PARAMS: MSDParameters = MSDParameters {
        mass: 100.,
        spring_constant: 30000.0,
        damping_constant: 1000.0,
        initial_force: 1000.0,
        initial_values: [0.0, 0.0],
    };

    let now = std::time::Instant::now();
    let result = run_all_msd(&BASE_PARAMS);
    let elapsed = now.elapsed();

    println!("elapsed: {:?}", elapsed);

    match result.write_csv("test_all.csv") {
        Ok(v) => {},
        Err(e) => panic!("Error while writing csv {:?}", e),
    };
}
