# Flask and MySQL microservices deployment on Kubernetes

This repository contains code that deploys two microservices, i.e:-
1. Deploys a Flask API to add, delete and modify users in the MySQL database
2. Deploys a MySQL server on kubernetes cluster
3. Attaches a persistent volume to it, so the data remains contained if pods are restarting

## Prerequisites
1. Have `Docker` and `Kubernetes CLI (kubectl)` installed together with `Minikube`.

## Setup
1. Clone the repository
2. Configure `Docker` to use the `Docker daemon` in your kubernetes cluster via your terminal: 
  `eval $(minikube docker-env)`
3. Pull the latest mysql image from Dockerhub: `Docker pull mysql`
4. Build a kubernetes-api image with the Dockerfile in this repo: `Docker build . -t flask-api`

## K8 Secrets
Kubernetes Secrets can store and manage sensitive information. For this example we will define a password for the `root`
user of the `MySQL` server using the `Opaque` secret type. 

1. Encode your password in your terminal: `echo -n super-secret-password | base64`
2. Add the output to the `flask-secrets.yml` file at the `db_root_password` field

## Deployments for the Flask and MySQL microservices
1. Add the secrets to your `kubernetes cluster: kubectl apply -f flask-secrets.yml`
2. Create the `persistent volume` and `persistent volume claim` for the database: `kubectl apply -f mysql-pv.yml`
3. Create the MySQL deployment: `kubectl apply -f mysql-deployment.yml`
4. Create the Flask API deployment: `kubectl apply -f flaskapp-deployment.yml`

## Databases and Schema
1. Connect to your `MySQL database` by setting up a temporary pod as a mysql-client: 
   `kubectl run -it --rm --image=mysql --restart=Never mysql-client -- mysql --host mysql --password=<super-secret-password>`
2. Create the database and table
   - `CREATE DATABASE flaskapi;`
   - `USE flaskapi;`
   - `USE flaskapi;`
   - `CREATE TABLE users(user_id PRIMARY KEY AUTO_INCREMENT, user_name VARCHAR(255), user_email VARCHAR(255), 
      user_password VARCHAR(255));`

## Expose the Flask API
The Flask API can be exposed and accessed by using: `minikube service flask-service` command. This returns a URL which you
can paste in the browser and see a `Welcome to my Flask Api` message. You can use this `service_URL` to make requests to
the API

## Making requests
You can use the API to perform `create, read, update and delete` operations to your database. You can use postman or curl
1. Add a user: `curl -H "Content-Type: application/json" -d '{"name": "<user_name>", 
   "email": "<user_email>", "password": "<user_password>"}' <service_URL>/add_user`
2. Get all users: `curl <service_URL>/get_users`
3. Get details of a specific user: `curl <service_URL>/get_user/<user_id>`
4. Delete a user by user_id: `curl -H "Content-Type: application/json" <service_URL>/delete_user/<user_id>`
5. update a user's information: `curl -H "Content-Type: application/json" -d {"name": "<user_name>", 
   "email": "<user_email>", "password": "<user_password>", "user_id": <user_id>} <service_URL>/update_user`