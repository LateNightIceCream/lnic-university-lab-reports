/* Server */
use std::time::Instant;
use std::io::prelude::*;
use std::str::from_utf8;
use std::mem::size_of;
use std::os::unix::net::UnixStream;

use rand::{distributions::Alphanumeric, Rng};


const MAX_CHARS: usize = 100000;
const SOCKET_PATH: &str = "/tmp/pvs_socket";


fn main() {

    let mut csv_writer = match csv::Writer::from_path("output.csv") {
        Ok(v) => v,
        Err(e) => panic!("Could not start csv writer: {:?}", e),
    };

    // csv header
    csv_writer.write_record(&["n", "time_us"]);

    // generate a string
    let random_string: String = rand::thread_rng()
        .sample_iter(&Alphanumeric)
        .take(MAX_CHARS)
        .map(char::from)
        .collect();

    let bytes = random_string.as_bytes();
    let MAX_BYTES: usize = std::mem::size_of_val(&*bytes);
    
    let mut rx_buf = [0; (MAX_CHARS as u64 *4) as usize];

    for i in (0..(MAX_BYTES as u64)).step_by(100) {
        let mut stream = match UnixStream::connect(SOCKET_PATH) {
            Ok(v) => v,
            Err(e) => {
                panic!("Couldn't connect to socket: {e:?}");
            }
        };

        let now = Instant::now();
        let count = stream.write(&bytes[..((i+1) as usize)]).unwrap();
        //println!("sent {} Bytes", count);
        let count = stream.read(&mut rx_buf).unwrap();
        //let response = String::from_utf8(rx_buf[..count].to_vec()).unwrap();
        //println!("{response}");
        //println!("received {} Bytes", count);
        let elapsed = now.elapsed();
        if i % 1000 == 0 {
            println!("{:?}", elapsed);
        }

        csv_writer.write_record(&[(i as u64).to_string(), elapsed.as_micros().to_string()]);
    }


    csv_writer.flush().unwrap();

}

