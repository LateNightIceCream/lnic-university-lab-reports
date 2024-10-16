/* Server */
use std::time::Instant;
use std::io::prelude::*;
use std::str::from_utf8;
use std::mem::size_of;
use std::os::unix::net::UnixStream;
use rand::{rngs::StdRng, RngCore, SeedableRng};


const BUFFER_SIZE: usize = 500000;
const SOCKET_PATH: &str = "/tmp/pvs_socket";


fn main() {

    let mut csv_writer = match csv::Writer::from_path("output.csv") {
        Ok(v) => v,
        Err(e) => panic!("Could not start csv writer: {:?}", e),
    };

    // csv header
    csv_writer.write_record(&["n", "time_us"]);

    let seed = [0u8; 32];
    let mut rng: StdRng = SeedableRng::from_seed(seed);
    let mut tx_bytes = [0u8; BUFFER_SIZE];
    rng.fill_bytes(&mut tx_bytes);
    
    let mut rx_buf = [0u8; BUFFER_SIZE]; // try playing with size

    const MAX_TX_BYTES: u64 = (BUFFER_SIZE as u64);
    
    for i in (0..MAX_TX_BYTES).step_by(100) {
        // need a new connection each time for some reason
        let mut stream = match UnixStream::connect(SOCKET_PATH) {
            Ok(v) => v,
            Err(e) => {
                panic!("Couldn't connect to socket: {e:?}");
            }
        };

        //println!("sending {i} bytes");

        let now = Instant::now();
        let i: usize = i as usize;
        let mut tx_remaining: usize = i;

        loop {

            //println!("tx_remaining: {tx_remaining}");

            if tx_remaining == 0 {
                break;
            }

            let tx_count = stream.write(&tx_bytes[(i - tx_remaining)..(i)]).unwrap();
            //println!("tx_count: {tx_count}");
            tx_remaining -= tx_count;


            let mut rx_remaining: usize = tx_count;
            loop {
                if rx_remaining == 0 {
                    break;
                }

                rx_remaining -= stream.read(&mut rx_buf).unwrap();
                //println!("rx_remaining: {rx_remaining}");
            }
        }

        let elapsed = now.elapsed();

        if i % 1000 == 0 {
            println!("{:?}", elapsed);
        }

        csv_writer.write_record(&[(i as u64).to_string(), elapsed.as_micros().to_string()]);

    }


    csv_writer.flush().unwrap();

}

