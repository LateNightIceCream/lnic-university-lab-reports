/* Server */
use std::time::Instant;
use std::io::prelude::*;
use std::os::unix::net::{UnixListener, UnixStream};
use std::path::{Path, PathBuf};
use std::process;

use komm_benchmark::common::AutoCloseSocket;


const BUFFER_SIZE: usize = 700000; // bytes

const SOCKET_PATH: &str = "/tmp/pvs_socket";


fn main() -> std::io::Result<()> {

    let socket = match AutoCloseSocket::<UnixListener>::bind(Path::new(SOCKET_PATH)) {
        Ok(v) => {
            println!("Successfully bound Unix Domain Socket to {}", SOCKET_PATH);
            v
        },
        Err(e) => panic!("Problem binding to socket: {:?}", e),
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

    Ok(())
}


fn handle_client(mut stream: UnixStream) {
    println!("new connection");
    let mut buf = [0; BUFFER_SIZE];
    loop {

        let rx_count: usize = stream.read(&mut buf).unwrap();
        //println!("rx_count: {rx_count}");

        if rx_count == 0 {
            break;
        }

        let mut tx_remaining: usize = rx_count;
        loop {

            if tx_remaining == 0 {
                break;
            }

            tx_remaining -= stream.write(&buf[(rx_count-tx_remaining)..rx_count]).unwrap();
            //println!("tx_remaining: {tx_remaining}");

        }
    }
}
