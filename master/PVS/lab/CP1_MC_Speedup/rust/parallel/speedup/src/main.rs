use std::time::Instant;

use csv;

use std::time::Duration;

use clap::{Parser, Subcommand};

mod msd;
use msd::{MSDParameters, MSDResult};

mod parapara;
use core_affinity::{get_core_ids, CoreId};


const DAMPING_MIN: f32 = 800.0;
const DAMPING_MAX: f32 = 1200.0;

const T_START: f32 = 0.0;
const T_END: f32 = 2.0;
const STEP_WIDTH: f32 = 0.01;


/// Mass-Spring-Damper parallel benchmark
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Total number of computations
    num_runs: usize,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Run on specific cores
    RunCores { cores: Vec<usize> },
    /// Run on all available cores
    RunAll,
    /// Run on all cores, increasing the core count each time
    RunStepped,
}


fn run_msd_mc(params: &MSDParameters) -> MSDResult {
    let my_param = params.with_random_damping(DAMPING_MIN, DAMPING_MAX);
    let result = msd::solve_msd_trajectory(&my_param, T_START, T_END, STEP_WIDTH);
    result
}


fn core_function_2(num_calcs: usize, params: &MSDParameters) -> MSDResult {

    let mut total_result = run_msd_mc(params);

    for _i in 1..num_calcs {
        let result = run_msd_mc(params);
        total_result.states = total_result.states + result.states;
    }

    total_result.states = total_result.states / (num_calcs as f32);
    total_result
}


fn run_all_msd(params: &'static MSDParameters, used_cores: &[CoreId], num_runs: usize) -> Result<MSDResult, std::io::Error> {

    let mut msd_threads = parapara::MSDThreads::new(used_cores, num_runs);
    msd_threads.spawn_threads(params, core_function_2);

    match msd_threads.join() {
        Ok(v) => Ok(v),
        Err(e) => Err(std::io::Error::new(std::io::ErrorKind::Other, format!("thread failed {:?}", e))),
    }

}


fn run_cores(params: &'static MSDParameters, cores: &[CoreId], num_runs: usize, save_result: bool) -> Duration {
    let now = Instant::now();
    let result = run_all_msd(&params, &cores, num_runs).expect("unsuccessful thread result");
    if save_result {
        result.write_csv("last_trajectory.csv").expect("error while writing csv");
    }
    now.elapsed()
}


fn run_stepped(params: &'static MSDParameters, cores: &[CoreId], num_runs: usize) {

    let mut durations = vec![];
    let mut core_nums = vec![];

    for n in 0..cores.len() {
        let cores: Vec<CoreId> = cores.iter().take(n+1).cloned().collect();
        println!("--------");
        println!("Executing on {:?} cores ...", cores.len());
        let elapsed = run_cores(params, &cores, num_runs, false);
        println!("Elapsed: {:?}", elapsed);
        core_nums.push(cores.len());
        durations.push(elapsed);
    }

    let mut csv_writer = csv::Writer::from_path("speeds.csv")
            .expect("error creating csv writer");
    csv_writer.write_record(&["cores", "time_ms"])
            .expect("error writing to csv");
    for (n, duration) in std::iter::zip(core_nums, durations) {
        csv_writer.write_record(&[n.to_string(), duration.as_millis().to_string()])
            .expect("error writing to csv");
    }
}


fn main() {

    const BASE_PARAMS: MSDParameters = MSDParameters {
        mass: 100.,
        spring_constant: 30000.0,
        damping_constant: 1000.0,
        initial_force: 1000.0,
        initial_values: [0.0, 0.0],
    };

    let args = Args::parse();
    let all_cores = get_core_ids().expect("No cores available");

    match &args.command {
        Commands::RunCores { cores } => {
            if cores.is_empty() {
                panic!("no cores specified");
            }

            let mut used_cores: Vec<CoreId> = all_cores.iter().filter(|cid| {
                cores.contains(&cid.id)
            }).cloned().collect();

            used_cores.dedup();

            run_cores(&BASE_PARAMS, &used_cores, args.num_runs, true);
        },
        Commands::RunAll => {
            run_cores(&BASE_PARAMS, &all_cores, args.num_runs, true);
        },
        Commands::RunStepped => {
            run_stepped(&BASE_PARAMS, &all_cores, args.num_runs);
        }
    }
}
