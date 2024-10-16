use clap::Parser;
use std::time::Instant;
use rand::prelude::*;

/// Simple Benchmark
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Number of iterations to perform
    #[arg(short, long)]
    #[clap(value_parser = clap::value_parser!(u32).range(1..=4000000000))]
    num_iterations: u32,
}


fn main() {
    let args = Args::parse();
    let now = Instant::now();

    let mut rng = rand::thread_rng();
    
    let array1: [f32; 4] = [rng.gen::<f32>(), rng.gen::<f32>(), rng.gen::<f32>(), rng.gen::<f32>()];
    let mut array2: [f32; 4] = [rng.gen::<f32>(), rng.gen::<f32>(), rng.gen::<f32>(), rng.gen::<f32>()];
    let mut array3: [f32; 4] = [0.0, 0.0, 0.0, 0.0];

    for _n in 0..args.num_iterations {
        array3[0] = array1[0] + array2[0];
        array3[1] = array1[1] + array2[1];
        array3[2] = array1[2] + array2[2];
        array3[3] = array1[3] + array2[3];

        array2[0] = array1[0] * array3[0];
        array2[1] = array1[1] * array3[1];
        array2[2] = array1[2] * array3[2];
        array2[3] = array1[3] * array3[3];
    }

    let elapsed = now.elapsed();
    const NUM_OPS: u32 = 8;

    println!("array: {:?}", array1);
    println!("array2: {:?}", array2);
    println!("array3: {:?}", array3);
    println!("time: {:?}", elapsed);
    println!("GFLOPS: {}", (args.num_iterations as f64) / elapsed.as_secs_f64() * (NUM_OPS as f64) * 10e-9);
}

