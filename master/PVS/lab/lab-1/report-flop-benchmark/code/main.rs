use clap::Parser;
use std::time::Instant;


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
    let mut result: f32 = 1.0;
    let now = Instant::now();

    for _n in 0..args.num_iterations {
        result = 1.00001 * result;
    }

    let elapsed = now.elapsed();

    println!("done! {} time: {:?}", result, elapsed);
    println!("GFLOPS: {}", (args.num_iterations as f64) / elapsed.as_secs_f64() * 10e-9);
}
