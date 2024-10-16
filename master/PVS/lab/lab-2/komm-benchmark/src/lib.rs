
pub mod common {
    use std::path::{Path, PathBuf};
    use std::os::unix::net::UnixListener;

    // wrapper around UnixListener::bind
    // https://stackoverflow.com/questions/40218416/how-do-i-close-a-unix-socket-in-rust
    pub struct AutoCloseSocket<ListenerType> {
        pub path: PathBuf,
        pub listener: ListenerType,
    }


    impl AutoCloseSocket<UnixListener> {
        pub fn bind(path: impl AsRef<Path>) -> std::io::Result<Self> {
            let path = path.as_ref().to_owned();
            // Result::map maps Result<T,E> to Result<U,E> where U is whatever the
            // expression inside map(...) returns
            UnixListener::bind(&path).map(|listener| AutoCloseSocket { path, listener })
        }
    }


    impl<ListenerType> Drop for AutoCloseSocket<ListenerType> {
        fn drop(&mut self) {
            // There's no way to return a useful error here
            let _ = std::fs::remove_file(&self.path).unwrap();
        }
    }

}
