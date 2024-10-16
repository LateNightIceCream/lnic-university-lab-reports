/* Server */
use std::time::Instant;
use std::io::prelude::*;
use std::os::unix::net::{UnixListener, UnixStream};
use std::path::{Path, PathBuf};
use std::process;

use komm_benchmark::common::AutoCloseSocket;


const MAX_BYTES: u64 = 100000;

const SOCKET_PATH: &str = "/tmp/pvs_socket";


fn main() -> std::io::Result<()> {

    let socket = match AutoCloseSocket::<UnixListener>::bind(Path::new(SOCKET_PATH)) {
        Ok(v) => {
            println!("Successfully bound Unix Domain Socket to {}", SOCKET_PATH);
            v
        },
        Err(e) => panic!("Problem binding to socket: {:?}", e),
    };

    let mut csv_writer = match csv::Writer::from_path("output_server.csv") {
        Ok(v) => v,
        Err(e) => panic!("Could not start csv writer: {:?}", e),
    };

    println!("Now listening for connections...");
    for mut stream in socket.listener.incoming() {
        match stream {
            Ok(stream) => {
                //println!("Connection success!");
                handle_client(stream);
            }
            Err(err) => {
                panic!("Connection failed! {:?}", err);
            }
        }
    }

    csv_writer.write_record(&["n", "time_us"]);

    csv_writer.flush().unwrap();

    //let borrowed_fd = std::os::fd::AsFd::as_fd(&listener);

    Ok(())
}


fn handle_client(mut stream: UnixStream) {
    let mut buf = [0; MAX_BYTES as usize];
    let count = stream.read(&mut buf).unwrap();
    //let response = String::from_utf8(buf[..count].to_vec()).unwrap();
    //println!("received \"{response}\" which is {} Bytes", count);
    //println!("received {} Bytes", count);
    let count = stream.write(&buf[..count]).unwrap();
    //println!("sent {} Bytes", count);
    //stream.write_all(&buf).unwrap();
    //println!("wrote byte back");
}
