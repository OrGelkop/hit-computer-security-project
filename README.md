# Computer security final project
The project is running on Heroku platform, and accessible through - https://hit-computer-security-project.herokuapp.com

## Run project locally
In order to run the project locally, the recommended way to do so is:  
1. Create a Python virtual environment with Python version 3.7.12.
2. Install all Python requirements in the virtual environment, by running the command:  
```shell
sudo pip install -r requirements.txt
```
3. Create **setenv.sh** file in the project root folder, with these contents:
```shell
export DATABASE_URL=<value>
export DEBUG_MODE=<value>
export HASH_SALT=<value>
export PORT=<value>
export MAIL_USERNAME=<value>
export MAIL_PASSWORD=<value>
```
3. Make sure to replace all values for the environment variables.  
4. Load the environment variables, by running the command:  
```shell
source setenv.sh
```
5. Now you are ready to run the project, simply type:  
```shell
python app.py
```
And access **http://localhost/$PORT** to view the application.

## Connect to database
In order to connect ot the database with PSQL client, use Docker container:    
```shell
docker run -it --name psql jbergknoff/postgresql-client $DATABASE_URL
```

## XSS
TODO

## SQL Injection
TODO

## Stride
TODO
