/* Server */
use std::time::Instant;
use std::net::{TcpListener, TcpStream};
use std::io::prelude::*;

const MAX_CHARS: u64 = 100000;

fn main() {

    let listener = match TcpListener::bind("127.0.0.1:57007") {
        Ok(v) => v,
        Err(e) => panic!("Problem binding to socket: {:?}", e),
    };

    let mut csv_writer = match csv::Writer::from_path("output_server.csv") {
        Ok(v) => v,
        Err(e) => panic!("Could not start csv writer: {:?}", e),
    };

    csv_writer.write_record(&["n", "time_us"]);

    
    let mut loopcount: u64 = 0;

    for stream in listener.incoming() {
        let stream = match stream {
            Ok(v) => v,
            Err(e) => panic!("Could not access tcp stream: {:?}", e),
        };

        let now = Instant::now();

        handle_connection(stream);

        let elapsed = now.elapsed();

        if loopcount % 100 == 0 {
            println!("{:?}", elapsed);
        }

        csv_writer.write_record(&[loopcount.to_string(), elapsed.as_nanos().to_string()]);

        loopcount += 1;
    }

    csv_writer.flush().unwrap();

}


fn handle_connection(mut stream: TcpStream) {
    let mut rx_buffer = [0; (MAX_CHARS * 4) as usize];
    let mut n: usize = 0;
    loop {
        n = stream.read(&mut rx_buffer).unwrap(); // should slice ? [n..end]
        if n == 0 {
            break;
        }
    }

    loop {
        n = stream.write(&mut rx_buffer).unwrap();
        if n == 0 {
            break;
        }
    }

    stream.flush().unwrap();
    //println!("{}", String::from_utf8_lossy(&buffer[..]));
}
