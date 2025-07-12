### ports for the micro services:

book-service : 8000
loan-service : 8001
stat-service : 8002
user-service : 8003

## Creating an image
- docker build -t book-service .   //Should have the Dockerfile in the current directory 

## Spinning a container from an image
- docker run -d -p 8000:8000 book-service  // -d for background. -p for mapping port 

## Creating docker network
  docker network create backend
  docker run -d --name book-service --network my-app-network book-image

### Image vs Container
# 🧱 Image
- A blueprint for a container.
- Includes the app, environment, and dependencies.
- Read-only.
- Created from a Dockerfile.
- 💡 Think of it like a class in programming.

# 📦 Container
- A running instance of an image.
- Has its own filesystem, processes, and network.
- You can create, start, stop, or delete it.
- 💡 Think of it like an object created from a class.


### Running docker-compose.yml file
- docker compose up --build
- docker compose down

# removing image
- docker rmi image_name -f  // if exists container
- docker rmi -f $(docker images -q) // removing all images. Have to close the containers though.

# removing container
- docker rm cid -f //if running
- docker system prune //erases all stopped container.
- docker rm -f $(docker ps -aq) // stop and remove all containers
