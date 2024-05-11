# Host Web Flask App locally and on EC2

## Getting Started
Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

#### Prerequisites
If you want to install locally:

- Install docker and docker-compose

If you want to host on AWS:

- Need AWS account

#### Installation locally 
1. **Clone the repository**
2. **Navigate into the project directory**
3. **Start up the docker-compose**
  ```
  docker compose up
  ```
4. **After the application starts, navigate to https://localhost**

5. **Stop and remove containers**
  ```
  docker compose down
  ```
  
6. **NGINX as a reverse-proxy (now works with self signed cert TODO):**
  ```
  https://localhost
  ```
#### Installation on EC2 AWS

1. **Build EC2 with CloudFormation using e2.yaml file**
2. **Connect to EC2 and navigate into the project directory**
3. **Start up the docker-compose to generate your certificates**
   docker-compose -f docker-compose-cert.yml up --build
4. **Navigate to the folder with your certificates, copy them, and paste them into AWS Secret Manager**
   /etc/letsencrypt/live/cappybara.pp.ua - path to your secrets
   
   Set secret names as follows:
   
   prod/flaskapp for privkey.pem
   prod/flaskapp2 for fullchain.pem
5. **Run two python scripts**
   python3 aws_key.py
   python3 aws_cert.py

6. **Restart docker-compose**
   
   docker-compose --file docker-compose.yml down
   
   docker-compose --file docker-compose.yml build
   
   docker-compose --file docker-compose.yml up

8. **Please note you should update DNS name with your new IP address**
9. **Your App is available with domain https://capybara.pp.ua/** 
  
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
