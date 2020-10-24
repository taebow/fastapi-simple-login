docker image ls | grep fsldb || docker build -t fsldb -f db.dockerfile .
docker run -d -p 5432:5432 -v $(pwd)/pgdata:/var/lib/postgresql/data fsldb:latest
