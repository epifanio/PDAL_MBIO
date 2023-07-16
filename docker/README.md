# Docker deployment

## Set up a docker environment

* see instructions at: [setting up docker on ubuntu](setup_docker.md)

## Build the Container

* From the root directory of this repository, run:

```bash
docker build -f docker/Dockerfile -t mbapi .
```

## Start the service

```bash
docker-compose -f docker/docker-compose up
```

Your app should now run on [http://localhost:80/doc](http://localhost:80/doc)

# Docker Deployment notes

* [`volumes` and `environment` variables](note_docker_compose_volumes_and_environment.md)
