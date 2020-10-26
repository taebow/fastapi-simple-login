[![travis-ci-build-status]][travis-ci]

# fastapi-simple-login
A fastapi simple user and login manager.

## Requirements

- Docker
- Python 3.8
- [Poetry](https://python-poetry.org/docs/)

## Dependencies

- FastAPI
- Sqlalchemy
- psycopg2
- uvicorn
- pytest

Only tested on Linux (Arch).

## Usage

After having checked the requirements and ensured docker is running.

**Install dependencies :**
```
make install
```


**Start the development database :**

```shell
make start-db
```

*It build and run a docker image `db.dockerfile` that starts a Postgresql 
server on port 5432.*


**Run the service endpoint :**

```
make serve
```

*It run the server at http://localhost:8080*


**Interactive documentation**

- SwaggerUI is running on http://localhost:8080/docs


**Default root user**

 - email : root@example.com
 - password: password


**Run the tests** 
```shell
make test
```
> :warning: This will wipe the database content.

## Endpoints:

**User management :**
- GET /users
- POST /users
- GET /users/\<email\>
- PUT /users/\<email\>
- DELETE /users/\<email\>

**Login**
- POST /login

**Testing endpoints**
- GET /resource/public
- GET /resource/protected


**Authorization header**

'Authorization" header == "Bearer \<token returned by login\>"

## Additional info on implementation

- Password is currently stored on its own in the database, no hash.


[travis-ci]: https://travis-ci.org/github/tteaka/fastapi-simple-login
[travis-ci-build-status]: https://travis-ci.org/tteaka/fastapi-simple-login.svg?branch=main