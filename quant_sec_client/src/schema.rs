// @generated automatically by Diesel CLI.

diesel::table! {
    user_emails (EmailId) {
        EmailId -> Integer,
        #[max_length = 100]
        Sender -> Varchar,
        SubjectLine -> Nullable<Text>,
        Body -> Nullable<Text>,
        #[max_length = 100]
        DateOfArrival -> Varchar,
    }
}
