# Docker deployment

## Set up a docker environment

* see instructions at: [setting up docker on ubuntu](setup_docker.md)

## Build the Container

* From the root directory of this repository, run:

```bash
docker build -f docker/Dockerfile -t dash_app .
```

## Start the service

```bash
docker-compose -f docker/docker-compose up
```

Your app should now run on [http://localhost:9000](http://localhost:9000)

# Docker Deployment notes

* [`volumes` and `environment` variables](note_docker_compose_volumes_and_environment.md)
