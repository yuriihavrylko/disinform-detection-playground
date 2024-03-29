## Projector Course Work: Disinformation Detection Service
A project aimed at disinformation detection. This repository outlines the steps involved in deploying the service using various technologies, testing and benchmarking, as well as implementing various machine learning methodologies.

Done during Projector course [Machine Learning in Production](https://prjctr.com/course/machine-learning-in-production)

## Table of Contents
- [Projector Course Work: Disinformation Detection Service](#projector-course-work-disinformation-detection-service)
- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Minio setup](#minio-setup)
- [Data](#data)
  - [DVC](#dvc)
  - [Label studio](#label-studio)
- [Model training](#model-training)
- [Model optimization](#model-optimization)
- [Streamlit](#streamlit)
- [Model serving](#model-serving)
  - [Fast API](#fast-api)
  - [Seldon](#seldon)
  - [Kserve](#kserve)
- [Tests](#tests)
- [Benchmarks](#benchmarks)
  - [File formats](#file-formats)
  - [Load testing](#load-testing)
- [POD autoscaling](#pod-autoscaling)
- [Kafka](#kafka)
- [Data drift detection](#data-drift-detection)


## Prerequisites
This guide assumes that you have basic knowledge in the following technologies:
- Docker
- GitHub Actions
- Kubernetes

## Minio setup
Mac/Local
```
brew install minio/stable/minio

minio server --console-address :9001 ~/minio # path to persistent local storage + run on custom port
```

Docker

```
docker run \
   -p 9002:9002 \
   --name minio \
   -v ~/minio:/data \
   -e "MINIO_ROOT_USER=ROOTNAME" \
   -e "MINIO_ROOT_PASSWORD=CHANGEME123" \
   quay.io/minio/minio server /data --console-address ":9002"
```

Kubernetes

```
kubectl create -f deployment/minio.yml
```

## Data

### DVC

Install DVC

```
brew install dvc
```

Init in repo

```
dvc init --subdir
git status
git commit -m "init DVC"
```

Move file with data and add to DVC, commit DBV data config

```
dvc add ./data/data.csv
git add data/.gitignore data/data.csv.dvc
git commit -m "create data"
```

Add remote data storage and push DVC remote config
(ensure that bucket already created)

```
dvc remote add -d minio s3://ml-data
dvc remote modify minio endpointurl [$AWS_ENDPOINT](http://10.0.0.6:9000)

git add .dvc/config
git commit -m "configure remote"
git push 
```

Upload data
```
export AWS_ACCESS_KEY_ID='...'
export AWS_SECRET_ACCESS_KEY='...'
dvc push
```

### Label studio

```
docker pull heartexlabs/label-studio:latest
docker run -it -p 8080:8080 -v `pwd`/mydata:/label-studio/data heartexlabs/label-studio:latest
```

![Alt text](assets/labeling.png)



## Model training 

Build
```
docker build -t model-training . -f job/Dockerfile
```

Run
```
docker run -it model-training
```

## Model optimization

Run pruning:

```
python -m src.model.pruning
```

Run distillation:

```
python -m src.model.distilation
```


## Streamlit 

Run:
```
streamlit run src/serving/streamlit.py
```

![Alt text](assets/streamlit.png)

Deploy k8s:
```
kubectl create -f deployment/app-ui.yml
kubectl port-forward --address 0.0.0.0 svc/app-ui.yml 8080:8080
```

Deploy k8s:
```
kubectl create -f deployment/app-ui.yml
kubectl port-forward --address 0.0.0.0 svc/app-ui.yml 8080:8080
```

## Model serving

### Fast API 

Postman

![Alt text](assets/fastapi.png)



Deploy k8s:
```
kubectl create -f deployment/app-fasttext.yml
kubectl port-forward --address 0.0.0.0 svc/app-fasttext 8090:8090
```

### Seldon

Installation

```
kubectl apply -f https://github.com/datawire/ambassador-operator/releases/latest/download/ambassador-operator-crds.yaml
kubectl apply -n ambassador -f https://github.com/datawire/ambassador-operator/releases/latest/download/ambassador-operator-kind.yaml
kubectl wait --timeout=180s -n ambassador --for=condition=deployed ambassadorinstallations/ambassador

kubectl create namespace seldon-system

helm install seldon-core seldon-core-operator --version 1.15.1 --repo https://storage.googleapis.com/seldon-charts --set usageMetrics.enabled=true --set ambassador.enabled=true  --namespace seldon-system
```

Deploy k8s:
```
kubectl create -f deployment/seldon-custom.yaml
```

### Kserve

Deploy k8s:

```
kubectl create -f deployment/kserve.yaml
kubectl get inferenceservice custom-model
```


## Tests

Run tests
```
pytest app/tests/
```

## Benchmarks

### File formats

![Alt text](assets/format_benchmark.png)

| Format   | Avg Write Time (s) | Avg Read Time (s) | File Size after Write (MB) |
|----------|--------------------|-------------------|----------------------------|
| CSV      | 0.906960           | 0.174510          | 5.649742                   |
| JSON     | 0.386252           | 1.161783          | 16.038124                  |
| PARQUET  | 0.061314           | 0.016811          | 1.507380                   |
| ORC      | 0.167490           | 0.016776          | 6.998336                   |



CSV format shows relatively slower write times compared to other formats, with a moderate file size after write.

JSON format demonstrates faster write times but slower read times compared to other formats, with the largest file size after write.

PARQUET format showcases the fastest write times and relatively fast read times, with a smaller file size after write compared to CSV and JSON.

ORC format exhibits moderate write times and the smallest file size after write among the tested formats, with efficient read times.


### Load testing

![Alt text](assets/locust.png)

```
locust -f benchmarks/load_test.py --host=http://localhost:9933 --users 50 --spawn-rate 10 --autostart --run-time 600s
```

## POD autoscaling

Install metric service

```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl patch -n kube-system deployment metrics-server --type=json -p '[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
```

Run from config

```
kubectl create -f deployment/app-fastapi-scaling.yml
```


## Kafka

Install kafka
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install zookeeper bitnami/zookeeper --set replicaCount=1 --set auth.enabled=false --set allowAnonymousLogin=true --set persistance.enabled=false --version 11.0.0
helm install kafka bitnami/kafka --set zookeeper.enabled=false --set replicaCount=1 --set persistance.enabled=false


# eventing
kubectl apply -f https://github.com/knative/eventing/releases/download/knative-v1.9.7/eventing-crds.yaml
kubectl apply -f https://github.com/knative/eventing/releases/download/knative-v1.9.7/eventing-core.yaml
kubectl apply -f https://github.com/knative-sandbox/eventing-kafka/releases/download/knative-v1.9.1/source.yaml
```

Run deployment

```
kubectl apply -f deployment/kafka-infra.yml

kubectl port-forward $(kubectl get pod --selector="app=minio" --output jsonpath='{.items[0].metadata.name}') 9000:9000

mc config host add myminio http://127.0.0.1:9000 miniominio miniominio

mc mb myminio/input
mc mb myminio/output

mc admin config set myminio notify_kafka:1 tls_skip_verify="off"  queue_dir="" queue_limit="0" sasl="off" sasl_password="" sasl_username="" tls_client_auth="0" tls="off" client_tls_cert="" client_tls_key="" brokers="kafka-headless.default.svc.cluster.local:9092" topic="test" version=""


mc admin service restart myminio
mc event add myminio/input arn:minio:sqs::1:kafka -p --event put --suffix .json

kubectl create -f deployment/kafka-infra.yml
```

## Data drift detection

```
python -m src.monitoring.drift
```

![Alt text](assets/drift.png)
