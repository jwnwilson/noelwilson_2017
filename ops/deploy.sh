#! /bin/bash
PROJECT_ID=jwnwilson-eu

#gcloud container clusters create web-cluster --num-nodes=2

make run-fe-build

gcloud auth application-default login

gcloud config set project $PROJECT_ID
gcloud config set compute/zone europe-west1-b

docker build -f ./ops/Dockerfile_server -t gcr.io/${PROJECT_ID}/web:v1 .
docker build -f ./ops/Dockerfile_mongo_setup -t gcr.io/${PROJECT_ID}/db:v1 .

gcloud docker -- push gcr.io/${PROJECT_ID}/web:v1
gcloud docker -- push gcr.io/${PROJECT_ID}/db:v1

gcloud container clusters get-credentials web-cluster

#kompose convert -f ./ops/kubernetes/docker-compose-deploy.yaml

kubectl create -f ./ops/kubernetes/db-data-persistentvolumeclaim.yaml

kubectl create -f ./ops/kubernetes/db-deployment.yaml
kubectl create -f ./ops/kubernetes/db-service.yaml

kubectl create -f ./ops/kubernetes/db-job.yaml

kubectl create -f ./ops/kubernetes/server-deployment.yaml
kubectl create -f ./ops/kubernetes/server-service.yaml
