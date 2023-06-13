# set up a docker environment

Installation instruction from the [Official Docker documentation](https://docs.docker.com/engine/install/ubuntu/)

## Uninstall old versions

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

## Install using the apt repository🔗

### Set up the repository

* 1) Update the `apt` package index and install packages to allow apt to use a repository over HTTPS:

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
```

* 2) Add Docker’s official GPG key:

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

* 3) Use the following command to set up the repository:

```bash
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Install Docker Engine

* 1) Update the `apt` package index:

```bash
sudo apt-get update
```

* 2) Install Docker Engine, containerd, and Docker Compose.

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

* 3) Verify that the Docker Engine installation is successful by running the `hello-world` image.

```bash
sudo docker run hello-world
```

## Linux post-installation steps for Docker Engine

* 1) Create the docker group.

```bash
sudo groupadd docker
```

* 2) Add your user to the docker group.

```bash
sudo usermod -aG docker $USER
```

* 3 Activate the changes to groups:

```bash
newgrp docker
```

* 4) Verify that you can run `docker` commands without `sudo`.

```bash
docker run hello-world
```
