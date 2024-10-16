
// Mass Spring Damper ODE module

use ndarray;
use rand::distributions::{Distribution, Uniform};
use csv;


#[derive(Debug)]
pub struct MSDParameters {
    pub mass: f32,
    pub spring_constant: f32,
    pub damping_constant: f32,
    pub initial_force: f32,
    pub initial_values: [f32; 2],
}


impl MSDParameters {
    pub fn with_random_damping(&self, min: f32, max: f32) -> MSDParameters {
        let step = Uniform::new(min, max);
        let choice = step.sample(&mut rand::thread_rng());
        MSDParameters {
            mass: self.mass,
            spring_constant: self.spring_constant,
            damping_constant: choice,
            initial_force: self.initial_force,
            initial_values: self.initial_values,
        }
    }
}


pub struct MSDResult {
    pub time_vec: ndarray::Array1<f32>,
    pub states: ndarray::Array2<f32>,
}


impl MSDResult {
    pub fn from_time_vec(time_vec: ndarray::Array1::<f32>) -> MSDResult {
        let n_points = time_vec.shape()[0];
        MSDResult {
            time_vec: time_vec,
            states: ndarray::Array2::zeros((n_points, 2))
        } 
    }

    pub fn num_points(&self) -> usize {
        self.time_vec.len()
    }

    pub fn write_csv(&self, filename: &str) -> Result<(), csv::Error> {
        let mut csv_writer = csv::Writer::from_path(filename)?;

        csv_writer.write_record(&["t", "x1", "x2"]);

        for i in 0..self.num_points() {
            csv_writer.write_record(&[
                                    self.time_vec[i].to_string(),
                                    self.states[[i, 0]].to_string(),
                                    self.states[[i, 1]].to_string()
            ]);
        }
        Ok(())
    }
}


/// Returns the derivative of the given state
fn msd_dot(state: &ndarray::ArrayView<f32, ndarray::Ix1>, param: &MSDParameters) -> ndarray::Array1<f32> {
    ndarray::array![
        state[1], 
        (param.initial_force - param.damping_constant * state[1] - param.spring_constant * state[0]) / param.mass
    ]
}


/// simple euler method
pub fn solve_msd_trajectory(param: &MSDParameters, t_start: f32, t_end: f32, step_width: f32) -> MSDResult {

    let mut result = MSDResult::from_time_vec(ndarray::Array1::range(t_start, t_end, step_width));

    result.states[[0,0]] = param.initial_values[0];
    result.states[[0,1]] = param.initial_values[1];

    for i in 1..result.num_points() {
        let xdot = msd_dot(&result.states.slice(ndarray::s![i-1, ..]), &param);
        result.states[[i, 0]] = result.states[[i-1, 0]] + step_width * xdot[0];
        result.states[[i, 1]] = result.states[[i-1, 1]] + step_width * xdot[1];
    }

    //println!("{:?}", result.states);

    result
}

