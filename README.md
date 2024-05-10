# Python/Flask application and a Mongo database

## Getting Started
Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

#### Prerequisites
- Install docker and docker-compose

#### Installation
1. **Clone the repository**
2. **Navigate into the project directory**
3. **Start up the docker-compose**
  ```
  docker compose up
  ```
**To rebuild container:**
  ```
  docker-compose up -d --build
  ```
4. **After the application starts, navigate to http://localhost:5050**

5. **Stop and remove containers**
  ```
  docker compose down
  ```
  
6. **NGINX as a reverse-proxy (now works with self signed cert):**
  ```
  https://localhost
  ```
  
## Swagger
**Uses route /docs by default**

Example URL
```
 http://localhost:5050/docs
```
**You can use Swagger UI to test your endpoints**

Swagger OpenAPI file location
```
~/backend/static/swagger.json
```
**Modify this file if you do some changes in any declared endpoints**
