# Computer security final project
The project is running on Heroku platform, and accessible through - https://hit-computer-security-project.herokuapp.com

## Run project locally
In order to run the project locally, you should create file **setenv.sh** with this content:  
```shell
export DATABASE_URL=<value>
export DEBUG_MODE=<value>
export HASH_SALT=<value>
```

In order to have psql client against the database, run a docker container from this image: https://hub.docker.com/r/jbergknoff/postgresql-client:  
```shell
docker run -it --name psql jbergknoff/postgresql-client $DATABASE_URL
```
