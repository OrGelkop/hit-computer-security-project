CREATE TABLE users (
   id SERIAL,
   email                       varchar(30)  NOT NULL PRIMARY KEY,
   display_name                varchar(60)  NOT NULL,
   password                    varchar(77)  NOT NULL,
   reset_password_next_login   int NOT NULL DEFAULT 0,
   login_retries               int NOT NULL DEFAULT 0,
   locked                      int NOT NULL DEFAULT 0,
   is_admin                    int NOT NULL DEFAULT 0,
   previous_passwords_list     varchar(77)[]
);