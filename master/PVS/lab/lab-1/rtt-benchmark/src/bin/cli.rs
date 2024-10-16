/* Server */
use std::time::Instant;
use std::net::{TcpListener, TcpStream};
use std::io::prelude::*;
use std::str::from_utf8;
use std::mem::size_of;


const START_CHARS: u64 = 1000;
const MAX_CHARS: u64 = 100000;


fn send_n_chars(stream: &mut TcpStream, character: char, n: u64) -> Result<usize, std::io::Error> {
    let send_str = character.to_string().repeat(n as usize);

    let send_bytes = send_str.as_bytes();

    stream.write(send_str.as_bytes())
}


fn main() {

    let mut csv_writer = match csv::Writer::from_path("output.csv") {
        Ok(v) => v,
        Err(e) => panic!("Could not start csv writer: {:?}", e),
    };

    // csv header
    csv_writer.write_record(&["n", "time_us"]);

    let mut rx_buffer = Vec::<u8>::with_capacity((MAX_CHARS*4) as usize);//[0u8; (MAX_CHARS*4) as usize];
    let mut rx_buffer = [0u8; (MAX_CHARS*4) as usize];

    for n in START_CHARS..(MAX_CHARS+1) {

        let mut stream = match TcpStream::connect("127.0.0.1:57007") {
            Ok(v) => v,
            Err(e) => panic!("Could not connect to target address: {:?}", e),
        };

        // send data
        match send_n_chars(&mut stream, '🐹', n) { // note: rust char is 4 bytes! 
            Ok(_) => {},
            Err(e) => panic!("Error while sending {} chars {:?}", n, e),
        };


        let now = Instant::now();

        loop {
            // receive data
            let num_bytes = match stream.read(&mut rx_buffer) {
                Ok(v) => {v},
                Err(e) => panic!("Error while reading from stream! {:?}", e),
            };

            if num_bytes == 0 {
                break;
            }
        }

        let elapsed = now.elapsed();

        if n % 100 == 0 {
            println!("buffer size: {}", rx_buffer.len());
            println!("loop count: {}", n);
            //println!("loop count: {}, received chars: {}", n, String::from_utf8_lossy(&rx_buffer));
            println!("{:?}", elapsed);
        }

        csv_writer.write_record(&[n.to_string(), elapsed.as_nanos().to_string()]);

    }

    csv_writer.flush().unwrap();

}

