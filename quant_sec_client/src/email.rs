use diesel::prelude::*;
use dotenv::dotenv;
use std::env;
use crate::schema::user_emails::dsl::*;
use diesel::mysql::MysqlConnection;
use std::cmp::min;

#[derive(Queryable)]
#[diesel(table_name = user_emails)]
pub struct UserEmails {
    pub email_id: i32,
    pub sender: String,
    pub subject_line: Option<String>,
    pub body: Option<String>,
    pub date_of_arrival: String
}

fn establish_connection() -> MysqlConnection {
    dotenv().ok();    
    
    let database_url = env::var("DATABASE_URL")
    .expect("DATABASE_URL must be set");

    MysqlConnection::establish(&database_url)
    .expect(&format!("Error connecting to {}", database_url))
}

pub fn get_emails() {
    let mut connection = establish_connection();
    
    let results: Vec<UserEmails> = user_emails
        .load::<UserEmails>(&mut connection)
        .expect("Error loading inbox");
    
    println!("Found {} email(s) in inbox \n", results.len());
    
    for i in 0..min(results.len(), 10) {
        println!("{}--> Sender: {:?}\nSubject: {:?}\nBody: {:?}\nDate of Arrival: {:?}\n"

            ,results[i].email_id
            ,results[i].sender
            ,match &results[i].subject_line {
                Some(s) => {
                    s.to_string()
                }
                None => {
                    "NULL".to_string()
                }
            }
            ,match &results[i].body {
                Some(s) => {
                    s.to_string()
                }
                None => {
                    "NULL".to_string()
                }
            }
            ,results[i].date_of_arrival
        );
    }
}

pub fn insert_email() {
    let mut connection = establish_connection();
    let _ = diesel::insert_into(user_emails)
        .values((
            Sender.eq("aarav".to_string()),
            SubjectLine.eq(Some("aarav is great".to_string())),
            Body.eq(Some("aarav".to_string())),
            DateOfArrival.eq("19th June".to_string())
        ))
        .execute(&mut connection);
}