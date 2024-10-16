use std::{time::Instant, thread::{self, JoinHandle}};
use rand::Rng;
use core_affinity::{self, get_core_ids};
use core_affinity::CoreId;
use std::io::Error;


fn get_core_task_amounts(total_tasks: usize, num_cores: usize) -> Vec<usize> {

    let mut amounts = vec![];

    for _i in 0..num_cores {
        amounts.push(total_tasks / num_cores);
    }

    let mut remainder = total_tasks % num_cores;
    for i in 0..num_cores {
        if remainder == 0 {
            break;
        }
        amounts[i] += 1;
        remainder -= 1;
    }

    amounts
}


fn core_function(num_calcs: usize, my_bound_param: f64) -> f64 {
    let mut sum: f64 = 0.0;
    for i in 0..num_calcs {
        sum += i as f64;
    }
    sum
}


// https://stackoverflow.com/questions/59646632/share-function-reference-between-threads-in-rust
fn spawn_threads(num_calcs: usize,
                 core_ids: &[CoreId],
                 fun: &'static (dyn Fn(usize) -> f64 + Send + Sync)) -> Result<Vec<JoinHandle<f64>>, Error> 
{

    let mut handles = vec![];
    let amounts = get_core_task_amounts(num_calcs, core_ids.len());

    let mut i = 0;
    for _cid in core_ids {
        let amount = amounts[i];
        let cid = core_ids[i];
        println!("Spawning thread on core with id {:?}", cid.id);
        handles.push(thread::spawn(move || {
            let res = core_affinity::set_for_current(cid);
            if res {
                fun(amount)
            } else {
                0.0
            }
        }));
        i += 1;
    }

    Ok(handles)
}


fn main() {
    const NUM_TASKS: usize = 10082;

    static my_bound_param: f64 = 2.0;

    if let Some(core_ids) = get_core_ids() {
        let handles = spawn_threads(NUM_TASKS, &core_ids[2..=3], &|amount: usize| {
            core_function(amount, my_bound_param)
        }).unwrap();

        for handle in handles {
            let s = handle.join().unwrap();
            println!("{s}");
        }
    }


    println!("main thrado done!");
}
