
// simple msd parallelization module

use std::{time::Instant, thread::{self, JoinHandle}, io::ErrorKind};
use core_affinity::CoreId;
use crate::msd::{MSDResult, MSDParameters};


#[derive(Debug)]
pub struct MSDThreads<'a> {
    core_ids: &'a [CoreId],
    total_tasks: usize,
    handles: Vec<JoinHandle<MSDResult>>,
}


impl<'a> MSDThreads<'a> {

    pub fn new(core_ids: &[CoreId], num_tasks: usize) -> MSDThreads {
        MSDThreads {
            core_ids: core_ids,
            total_tasks: num_tasks,
            handles: vec![],
        }
    }


    pub fn num_cores(&self) -> usize {
        self.core_ids.len()
    } 


    pub fn spawn_threads(&mut self, params: &'static MSDParameters, func: fn(usize, &MSDParameters) -> MSDResult) {
        let amounts = self.get_core_task_amounts();

        let mut i = 0;
        for cid in self.core_ids.to_owned() {
            let params = params.clone();
            let amount = amounts[i];

            println!("Spawning thread with {:?} tasks on core with id {:?}",
                     amount, cid);

            let h = thread::spawn(move || {
                let res = core_affinity::set_for_current(cid);
                func(amount, params)
            });

            self.handles.push(h);

            i += 1;
        }
    }


    pub fn join(self) -> std::thread::Result<MSDResult> {
        let mut results = vec![];
        for handle in self.handles {
            results.push(handle.join()?);
        }

        let num_results = results.len();
        // TODO
        /*if num_results == 0 {
            println!("no resultos!");
        }*/

        // average all results
        let mut total_result = MSDResult::from_time_vec(results[0].time_vec.clone());
        for result in results {
            total_result.states = total_result.states + result.states;
        }

        total_result.states = total_result.states / (num_results as f32);

        Ok(total_result)
    }


    fn get_core_task_amounts(&self) -> Vec<usize> {
        let mut amounts = vec![];
        let ncores = self.num_cores();

        for _i in 0..ncores {
            amounts.push(self.total_tasks / ncores);
        }

        let mut remainder = self.total_tasks % ncores;
        for i in 0..ncores {
            if remainder == 0 {
                break;
            }
            amounts[i] += 1;
            remainder -= 1;
        }

        amounts
    }
}



/*
// https://stackoverflow.com/questions/59646632/share-function-reference-between-threads-in-rust
pub fn spawn_threads(num_calcs: usize,
                 core_ids: &[CoreId],
                 fun: &'static (dyn Fn(usize) -> msd::MSDResult + Send + Sync)) -> Result<Vec<JoinHandle<Option<msd::MSDResult>>>, Error> 
{

    let mut handles = vec![];
    let amounts = get_core_task_amounts(num_calcs, core_ids.len());

    let mut i = 0;
    for _cid in core_ids {
        let amount = amounts[i];
        let cid = core_ids[i];
        println!("Spawning thread with {:?} tasks on core with id {:?}", amount, cid.id);
        handles.push(thread::spawn(move || {
            let res = core_affinity::set_for_current(cid);
            if res {
                Some(fun(amount))
            } else {
                None
            }
        }));
        i += 1;
    }

    Ok(handles)
}
*/
