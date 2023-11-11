mod email;
mod schema;
mod utils;

use rustyline::error::ReadlineError;
use rustyline::{DefaultEditor, Result};
use crate::email::{get_emails};

static mut SHOULD_CONTINUE: bool = true;

fn handle_command(cmnd : &str) {
    match cmnd {
        "connect" => {
            // Connect to a server using it's IP address
        },
        "create-account" => {
            // Create a user account with unique userID and password
            // It also creates a unique crystal-kyber public key 
        },
        "login" => {
            // Login a user with userId and password
        },
        "sync" => {
            // imports all the emails
        },
        "list-emails" => {
            // lists all the emails recieved to the user (requires a login)
            get_emails();
        },
        "send" => {
            // send an email to a user using it's unique userID
        },
        "clear-inbox" => {
            // delete all emails
        }
        "exit" => {
            unsafe {
                SHOULD_CONTINUE = false;
            }
            println!("Exiting...");
        },
        x => {
            println!("\x1b[31;1mUnknown command: \x1b[0m{}", x);
        }
    }
}

fn main() -> Result<()> {
    let mut rl = DefaultEditor::new()?;

    #[cfg(feature = "with-file-history")]
    if rl.load_history("history.txt").is_err() {
        println!("No previous history is available.");
    }
    println!("Welcome!");

    loop {
        let readline = rl.readline("\x1b[35;1m> \x1b[0m");

        match readline {
            Ok(line) => {
                let _ = rl.add_history_entry(line.as_str());
                handle_command(line.as_str());
            },
            Err(ReadlineError::Interrupted) | Err(ReadlineError::Eof) => {
                println!("Exiting....");
                break;
            },
            Err(error) => {
                println!("\x1b[31;1mError: \x1b[0m{:?}", error);
                break;
            }
        }
        unsafe {
            if !SHOULD_CONTINUE {
                break;
            }
        }
    }

    #[cfg(feature = "with-file-history")]
    let _ = rl.save_history("history.txt");
    Ok(())
}