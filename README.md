# Computer security final project
The project is up and running on thanks to Heroku platform.

There are 2 main branches:
1. main - The main and secured branch which gives solutions to the security vulnerabilities.  
Main branch url - https://hit-computer-security-project.herokuapp.com/
2. insecure - The branch which we demonstrate the XSS and SQL Injection vulnerabilities.
Insecure branch url - https://hit-insecure-security-project.herokuapp.com/

## Run project locally
In order to run the project locally, the recommended way to do so is:  
1. Create a Python virtual environment with Python version 3.7.12.
2. Install all Python requirements in the virtual environment, by running the command:  
```shell
# Linux
sudo pip install -r requirements.txt

# Windows
pip install -r requirements.txt
```
3. Create **setenv.sh** file in the project root folder, with environment variables, and replace the values:
```shell
# Linux
export DATABASE_URL=<value>
export DEBUG_MODE=<value>
export HASH_SALT=<value>
export PORT=<value>
export MAIL_USERNAME=<value>
export MAIL_PASSWORD=<value>

# Windows
set DATABASE_URL=<value>
set DEBUG_MODE=<value>
set HASH_SALT=<value>
set PORT=<value>
set MAIL_USERNAME=<value>
set MAIL_PASSWORD=<value>
```
4. Load the environment variables, by running the command:  
```shell
# Linux
source setenv.sh

# Windows
setenv.sh
```
5. Now you are ready to run the project, just branch out to the desired branch (main/insecure) and run: 
```shell
python app.py
```

## Connect to database
In order to have PSQL client against the database, use Docker container:    
```shell
docker run -it --name psql jbergknoff/postgresql-client $DATABASE_URL
```

## XSS
Cross-site scripting (XSS) is a security vulnerability which gives the ability to inject client-side scripts into web pages.  
By doing that, attackers can make the website run undesired code.  
For example, if you put the string 
```
<script>setInterval("alert(\"cryptomining :)\")",5000)</script>
```
as customer name or address, inside **add customer** form, once you load the home page, you will receive Javascript alert.  
We overcome this issue by using the autoescape feature which is built in Flask framework of Python.

## SQL Injection
SQL Injection is a code injection technique which executes malicious SQL statements against a relational database.  
We overcome this issue by not using string concatenation, as stated in the psycopg2 Python library:  
https://www.psycopg.org/docs/usage.html#the-problem-with-the-query-parameters

### Examples  
Page | Input field | Value | Outcome 
--- | --- | --- | --- 
Login | email | ```' OR ''='``` | Receive information of all existing users in the system
Register | display name | ```display_name'); delete from customers where (''='``` | Prune customers table content 
Add customer | address | ```address'); delete from users where (''='``` | Prune users table content 
